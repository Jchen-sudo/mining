创建流：
module Foo;
export {

    redef enum Log::ID += { LOG };

    # Define the record type that will contain the data to log.
    type Info: record {
        ts: time        &log;
        id: conn_id     &log;
        service: string &log &optional;
        missed_bytes: count &log &default=0;
    };
}
redef record connection += {
    foo: Info &optional;
};
event zeek_init() &priority=5
{
    Log::create_stream(Foo::LOG, [$columns=Info, $path="foo"]);
}
#发送数据到日志框架中
event connection_established(c: connection)
{
    local rec : Foo::Info = [$ts=network_time(), $id=c$id];
  
    # 将数据副本存储在connection record记录中，
    # 以便其他事件处理程序可以访问该数据。
    c$foo = rec;

    # 写入到了上文创建的流`Foo:LOG`
    Log::write(Foo::LOG, rec);
}
#`&log`没有这个属性，字段将不会出现在日志输出中.
#`&optional`属性也用于字段，这表明在日志写入记录之前，这个字段可能没有任何值
#`&default`属性的字段，能够自动初始化默认值
定义触发事件:
module Foo;
export {
    redef enum Log::ID += { LOG };
    type Info: record {
        ts: time     &log;
        id: conn_id  &log;
        service: string &log &optional;
        missed_bytes: count &log &default=0;
    };
    # Define a logging event. By convention, this is called
    # "log_<stream>".
    global log_foo: event(rec: Info);
} 
event zeek_init() &priority=5
{
    # 在此处指定 Foo 事件，以便 Zeek 触发（raise）该事件。
    Log::create_stream(Foo::LOG, [$columns=Info, $ev=log_foo,
                       $path="foo"]);
}
过滤器定义：

event zeek_init()
{
    # Add a new filter to the Conn::LOG stream that logs only
    # timestamp and originator address.
    local filter: Log::Filter = [$name="orig-only", $path="origs",
                                 $include=set("ts", "id.orig_h")];
    Log::add_filter(Conn::LOG, filter);
}
#获取默认过滤器更改path属性，再将其添加到该流的过滤器中
event zeek_init()
{
    # Replace default filter for the Conn::LOG stream in order to
    # change the log filename.
    local f = Log::get_filter(Conn::LOG, "default");
    f$path = "myconn";
    Log::add_filter(Conn::LOG, f);
}
#定义函数对应不同情况将日志流写入到不同日志中：

redef Site::local_nets = { 192.168.0.0/16 };
function myfunc(id: Log::ID, path: string, rec: Conn::Info) : string
{
    # Return "conn-local" if originator is a local IP, otherwise
    # return "conn-remote".
    local r = Site::is_local_addr(rec$id$orig_h) ? "local" : "remote";
    return fmt("%s-%s", path, r);
}
event zeek_init()
{
    local filter: Log::Filter = [$name="conn-split",
             $path_func=myfunc, $include=set("ts", "id.orig_h")];
    Log::add_filter(Conn::LOG, filter);
}
#标记长连接：
redef enum Notice::Type += {
    ## Indicates that a connection remained established longer
    ## than 5 minutes.
    Long_Conn_Found
};
event Conn::log_conn(rec: Conn::Info)
{
    if ( rec?$duration && rec$duration > 5mins )
        NOTICE([$note=Long_Conn_Found,
                $msg=fmt("unusually long conn to %s", rec$id$resp_h),
                $id=rec$id]);
}


