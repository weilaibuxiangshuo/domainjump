layui.use(['table','form','layer'], function () {
            var table = layui.table,form=layui.form,layer=layui.layer;
            var token = $('[name="csrfmiddlewaretoken"]').val();
            var tableIns=table.render({
                elem: '#index-test'
                , url: indexdata
                , toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
                , defaultToolbar: []
                , title: '用户数据表'
                , cols: [[
                    {type: 'checkbox', fixed: 'left'}
                    , {field: 'id', title: 'ID', width: 80, fixed: 'left', unresize: true, sort: true}
                    , {field: 'username', title: '用户名称', }
                    , {field: 'target', title: '跳转地址',}
                    , {fixed: 'right', title: '操作', toolbar: '#barDemo', width: 150}
                ]]
                , page: true
                ,done:function (res) {
                    var nbsp = "&nbsp&nbsp&nbsp";
                    $('#layui-card-header-text2').html("跳转目标：" + res.userurl);
                    $('#layui-card-header-text1').html("总数：" + res.usercount + nbsp + "剩余：" + res.surplus);
                },
            });



            //头工具栏事件
            table.on('toolbar(index-test)', function (obj) {
                var checkStatus = table.checkStatus(obj.config.id);
                switch (obj.event) {
                    case 'getCheckData':
                        var data = checkStatus.data;
                        layer.open({
                            type: 2,
                            content: createindex,
                            area: ['450px', '300px'],
                            btn: ['确定', '取消'],
                            yes:function (index, layero) {
                                var body=layer.getChildFrame('body',index);
                                var title1="",title2="",title3="";
                                title1=body.find('#input-textarea').val();
                                title2=$('#index-card-data').attr('title');
                                ////console.log(title2,'title2');
                                $.ajax({
                                    url:indexdata,
                                    method:'post',
                                    headers: {"X-CSRFToken": token},
                                    cache:false,
                                    data:{
                                        data:JSON.stringify([title1,title2])
                                    },
                                    success: function (obj) {
                                        if (obj.code !== 0){layer.msg(obj.code)};
                                        table.reload('index-test', {url: indexdata});
                                    }
                                });
                                layer.close(index);
                            },
                        });
                        break;
                }
                ;
            });

            //监听行工具事件
            table.on('tool(index-test)', function (obj) {
                var data = obj.data;
                //console.log(data.id);
                if (obj.event === 'del') {
                    layer.confirm('真的删除行么', function (index) {
                        $.ajax({
                            url:indexdata,
                            headers: {"X-CSRFToken": token},
                            method: "delete",
                            data:{data:data.id},
                            success:function () {
                                table.reload('index-test',{url:indexdata})
                            }
                        });
                        layer.close(index);
                    });
                } else if (obj.event === 'edit') {
                    layer.prompt({
                        formType: 2
                        , value: data.email
                    }, function (value, index) {
                        obj.update({
                            email: value
                        });
                        layer.close(index);
                    });
                }
            });
        });
