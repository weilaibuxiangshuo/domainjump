layui.use(['table','form','layer'], function () {
            var table = layui.table,form=layui.form,layer=layui.layer;
            var num1='',num2='',num3='';
            var token = $('[name="csrfmiddlewaretoken"]').val();
            table.render({
                elem: '#test'
                , url: mainindexdata
                , toolbar: '#toolbarDemo' //开启头部工具栏，并为其绑定左侧模板
                , defaultToolbar: []
                , title: '用户数据表'
                , cols: [[
                    {type: 'checkbox', fixed: 'left'}
                    , {field: 'id', title: 'ID', width: 80, fixed: 'left', unresize: true, sort: true}
                    , {field: 'username', title: '用户名', }
                    , {field: 'target', title: '跳转地址',}
                    , {fixed: 'right', title: '操作', toolbar: '#barDemo', width: 150}
                ]]
                , page: true
            });

            //头工具栏事件
            table.on('toolbar(test)', function (obj) {
                var checkStatus = table.checkStatus(obj.config.id);
                switch (obj.event) {
                    case 'getCheckData':
                        var data = checkStatus.data;
                        layer.open({
                            type: 2,
                            content: createmain,
                            area: ['450px', '370px'],
                            btn: ['确定', '取消'],
                            yes:function (index, layero) {
                                var body=layer.getChildFrame('body',index);
                                var title1="",title2="",title3="",title5="";
                                title1=body.find('#input-title1').val();
                                title2=body.find('#input-title2').val();
                                title5=body.find('#input-title5').val();
                                title3=body.find('input[type="radio"]:checked').val();
                                $.ajax({
                                    url:mainindexdata,
                                    method:'post',
                                    headers: {"X-CSRFToken": token},
                                    cache:false,
                                    data:{
                                        data:JSON.stringify([title1,title2,title3,title5])
                                    },
                                    success:function () {
                                        window.location.reload();
                                    }
                                });
                                layer.close(index);
                            },
                        });
                        break;
                    case 'EditCheckData':
                        var projectname=$('#maintest').find("option:selected").text();
                        if (projectname===""){layer.msg("请先选择账户",{icon:6});return false;}else {
                        var data = checkStatus.data;
                        layer.open({
                            type: 2,
                            content: editmain,
                            area: ['450px', '420px'],
                            btn: ['确定', '取消'],
                            success:function(layero, index){
                                var body=layer.getChildFrame('body',index);
                                body.find('#input-title1').val(projectname);
                                body.find('#input-title2').val(num1);
                                body.find('#input-title5').val(num2);
                                var tt=body.find('input[type="radio"]');
                                for (var b=0;b<tt.length;b++){
                                    if($(tt[b]).val()===num3){$(tt[b]).attr('checked', 'checked')};
                                }
                                var iframeWin = layero.find('iframe')[0].contentWindow;
                                iframeWin.layui.form.render('radio');
                            },
                            yes:function (index, layero) {
                                var body=layer.getChildFrame('body',index);
                                var title1="",title2="",title3="",title5="";
                                title1=body.find('#input-title1').val();
                                title2=body.find('#input-title2').val();
                                title5=body.find('#input-title5').val();
                                title3=body.find('input[type="radio"]:checked').val();
                                deleteuser=body.find('input[type="checkbox"]:checked').attr('name');
                                if (deleteuser==="deleteuser"){
                                    $.ajax({
                                        url:parentdata,
                                        method:'delete',
                                        headers: {"X-CSRFToken": token},
                                        cache:false,
                                        data:{data:title1},
                                        success:function (obj) {
                                            if(obj.code===0){window.location.reload()}
                                        }
                                    })
                                }else{
                                    $.ajax({
                                        url:mainindexdata,
                                        method:'post',
                                        headers: {"X-CSRFToken": token},
                                        cache:false,
                                        data:{
                                            data:JSON.stringify([title1,title2,title3,title5])
                                        },
                                        success:function () {
                                            window.location.reload();
                                        }
                                });}
                                layer.close(index);
                            },
                        });}
                        break;
                    case 'addall':
                        var projectname=$('#maintest').find("option:selected").text();
                        if (projectname===""){layer.msg("请先选择账户",{icon:6});return false;}else {
                        var data = checkStatus.data;
                        if (parseInt(num3)===3){
                            layer.open({
                            type: 2,
                            content: createjump,
                            area: ['450px', '350px'],
                            btn: ['确定', '取消'],
                            yes:function (index, layero) {
                                var body=layer.getChildFrame('body',index);
                                var title1="",title2="",title3="",title5='';
                                title1=body.find('#input-textarea').val();
                                title2=$('#maintest').find("option:selected").text();
                                title3=body.find('#input-title').val();
                                if (title2===""){layer.msg("请先选择项目",{icon:6});return false;}
                                if (title1==="" || title3===""){layer.msg("请输入内容",{icon:5});return false;}
                                //console.log(title2,'title2');
                                $.ajax({
                                    url:jumpindexdata,
                                    method:'post',
                                    headers: {"X-CSRFToken": token},
                                    cache:false,
                                    data:{
                                        data:JSON.stringify([title1,title2,title3])
                                    },
                                    success: function (obj) {
                                        //console.log(obj);
                                        if (obj.code !== 0){layer.msg(obj.code)};
                                        table.reload('test', {url: indexdata,where:{setuser:title2}});
                                    }
                                });
                                layer.close(index);
                            },
                        });
                        }else {
                            layer.open({
                            type: 2,
                            content: createindex,
                            area: ['450px', '300px'],
                            btn: ['确定', '取消'],
                            yes: function (index, layero) {
                                var body = layer.getChildFrame('body', index);
                                var title1 = "", title2 = "", title3 = "";
                                title1 = body.find('#input-textarea').val();
                                title2 = $('#maintest').find("option:selected").text();
                                if (title1===""){layer.msg("请输入内容",{icon:5});return false;}
                                if (title2===""){layer.msg("请先选择项目",{icon:6});return false;}else {
                                $.ajax({
                                    url: indexdata,
                                    method: 'post',
                                    headers: {"X-CSRFToken": token},
                                    cache: false,
                                    data: {
                                        data: JSON.stringify([title1, title2])
                                    },
                                    success: function (obj) {
                                        if (obj.code !== 0){layer.msg(obj.code)};
                                        table.reload('test', {url: indexdata,where:{setuser:title2}});
                                    }
                                })}
                                layer.close(index);
                            },
                        });
                        }}
                        break;
                    case 'delall':
                        var projectname=$('#maintest').find("option:selected").text();
                        if (projectname===""){layer.msg("请先选择账户",{icon:6});return false;}else {
                        var data = checkStatus.data;
                        var dataid=[];
                        for(var k=0;k<data.length;k++){
                            dataid.push(data[k].id)
                        }
                        layer.confirm('真的删除行么', function (index) {
                            $.ajax({
                                url: mainindexdata,
                                headers: {"X-CSRFToken": token},
                                method: "delete",
                                data: {data: JSON.stringify(dataid)},
                                success: function () {
                                    table.reload('test', {url: mainindexdata})
                                }
                            });
                        layer.close(index);
                        })}
                        break;
                    case 'logout':
                        $.ajax({
                            url:logout,
                            cache: false,
                        });
                        break;
                }
                ;
            });

            //监听行工具事件
            table.on('tool(test)', function (obj) {
                var data = obj.data;
                if (obj.event === 'del') {
                    layer.confirm('真的删除行么', function (index) {
                        $.ajax({
                            url:mainindexdata,
                            headers: {"X-CSRFToken": token},
                            method: "delete",
                            data:{data:JSON.stringify([data.id])},
                            success:function () {
                                table.reload('test',{url:mainindexdata})
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

            //监听form
            form.on('select(maintest)', function (data) {
                table.reload('test',{
                    url:mainindexdata,where:{data:data.value},page:{curr:1},done:function(res){
                        var nbsp="&nbsp&nbsp&nbsp";
                        $('#layui-card-header-text2').html("跳转目标："+res.userurl);
                        $('#layui-card-header-text1').html("总数："+res.usercount+nbsp+"剩余："+res.surplus+nbsp+"方式："+res.usermode);
                        num1=res.userurl;num2=res.usercount;num3=res.usermode;
                    }
                });
            });
        });
