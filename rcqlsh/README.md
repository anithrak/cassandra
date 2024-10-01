Note: 
- This is test/POC code 
- Not to be used in production

# Steps to connect with bodega from local

- Import project in pycharm
- Activate venv
- Install requirements

## Dependencies
Only cqlsh pip dependency is used

## Tunnel from local to bodega cqlproxy
ssh -i /Users/abhishek/Documents/code/sdmain/deployment/ssh_keys/ubuntu.pem -L localhost:9042:127.0.0.1:27577 ubuntu@10.0.35.91 

## run on terminal
python3 rcqlsh.py

## Should see something like
```commandline
(.venv) ➜  test-cqlsh python3 rcqlsh.py
/Users/abhishek/PycharmProjects/test-cqlsh/..
['/Users/abhishek/PycharmProjects/test-cqlsh/../lib']
['rcqlsh.py', '--protocol-version=4', '--cqlversion=3.4.0']
WARNING: cqlsh was built against 5.0.0, but this server is 3.0.9.  All features may not work!
Connected to Cqlproxy Cluster at 127.0.0.1:9042
[cqlsh 6.2.0 | Cassandra 3.0.9 | CQL spec 3.4.0 | Native protocol v4]
Use HELP for help.
```


## Query response 

`use sd;
expand on;
select * from files limit 10;`

```
@ Row 10
---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 uuid                | 56451a9266152016
 stripe_id           | -1
 birth_time          | 1727731502
 child_map           | null
 ctime               | 1727731517
 directory_spec      | {"1":{"i32":1},"2":{"lst":["str",0]},"3":{"rec":{"1":{"i32":2},"2":{"i32":2},"3":{"i32":0},"4":{"i32":134217728},"5":{"i32":4},"6":{"i32":2},"7":{"i32":131072},"8":{"i32":2},"9":{"lst":["str",0]}}},"4":{"tf":1},"5":{"str":""},"6":{"tf":0},"7":{"i64":0},"8":{"map":["str","rec",0,{}]},"9":{"str":""},"10":{"tf":1},"12":{"tf":0},"13":{"tf":0},"14":{"rec":{"1":{"tf":0},"2":{"i64":0}}},"15":{"tf":1},"17":{"tf":0}}
 file_spec           | 
 file_spec_v2        | {"1":{"i32":1},"2":{"str":""},"3":{"rec":{"1":{"map":["i64","rec",0,{}]},"2":{"i64":0},"3":{"i32":1},"4":{"tf":0},"5":{"tf":1},"6":{"tf":0},"7":{"str":""},"8":{"tf":1},"9":{"i32":0},"10":{"tf":0},"11":{"tf":0},"12":{"tf":0},"13":{"tf":0},"14":{"i32":1},"15":{"map":["i32","rec",0,{}]}}},"4":{"str":""}}
 history_serialized  | {"1":{"lst":["rec",5,{"1":{"i32":0},"2":{"i64":1727731502},"3":{"str":"vm-machine-u4yu77-rvrgvn6"},"4":{"str":"{ \"name\": \"1727731487\", \"job_instance\": \",,0\" }"}},{"1":{"i32":1},"2":{"i64":1727731502},"3":{"str":"vm-machine-u4yu77-rvrgvn6"},"4":{"str":"{\"size\": 2954}"}},{"1":{"i32":2},"2":{"i64":1727731517},"3":{"str":"vm-machine-u4yu77-rvrgvn6"},"4":{"str":"{ \"parent\": \"fe42c6e157c62f04\", \"name\": \"1727731487\", \"job_instance\": \",,0\" }"}},{"1":{"i32":3},"2":{"i64":1727731517},"3":{"str":"vm-machine-u4yu77-rvrgvn6"},"4":{"str":""}},{"1":{"i32":4},"2":{"i64":1727731517},"3":{"str":"vm-machine-u4yu77-rvrgvn6"},"4":{"str":""}}]}}
 internal_timestamp  | 1727731517872564
 last_modifier       | vm-machine-u4yu77-rvrgvn6
 linearizer          | null
 lock                | null
 metadata_version    | 1
 mode                | 33152
 mtime               | 1727731502
 open_heartbeat_time | null
 parent_map          | {"1":{"map":["str","map",1,{"fe42c6e157c62f04":["str","i32",1,{"1727731487":1}]}]}}
 parent_uuid_hint    | fe42c6e157c62f04
 size                | 2954
 state               | 2
 stripe_metadata     | null
 symlink_target      | null

(10 rows)

```