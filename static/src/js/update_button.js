function myFun(button) {
//    Here is the Js function for updating the chunks of Blog paragraphs
    console.log("button triggered")
    var button_id = button.id;
    var ai_content = button.nextSibling.textContent.trim();
    var blog_id = button.getAttribute('data-blog-id');
    var blog_post_id = button.getAttribute('data-blog-post-id');

//    We use AJAX for calling our controller for updating the blog content
    $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/update/blogBlock/',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                'jsonrpc': "2.0", 'method': "call",
                "params": {button_id,ai_content,blog_id,blog_post_id}
            }),
            success: function (message) {
               console.log(message);
            },
            error: function (data) {
               console.log(message);
            }
        });
//  Making the button invisible after 1 click
    button.style.display = 'none';

};

// This code will help us in later
//function myFunction() {
//    var old_employee_id = document.getElementById('old_employee_id').value;
//    var task_changing_reason = document.getElementById('task_changing_reason').value;
//    var select_employee_task = document.getElementById('employee_task');
//    var select_employee_project = document.getElementById('employee_projects');
//    var employee_project_id = select_employee_project.options[select_employee_project.selectedIndex].value;
//    var employee_task_id = select_employee_task.options[select_employee_task.selectedIndex].value;
//    var selected_employee = document.getElementById('all_employees');
//    var employee_id = selected_employee.options[selected_employee.selectedIndex].value;
//    var getResultTask = document.getElementById("myCheckTask");
//    var getResultProject = document.getElementById("myCheckProject");
//    var task_value=getResultTask.value;
//    var project_value=getResultProject.value;
//    var stage_id = document.getElementById('stage_id').value;
//
//    if (task_changing_reason == ''){
//        alert('Please Add a Reason');
//        document.getElementById("task_changing_reason").focus();
//    }
//    else{
//        $.ajax({
//            type: "POST",
//            dataType: 'json',
//            url: '/assign/task/',
//            contentType: "application/json; charset=utf-8",
//            data: JSON.stringify({
//                'jsonrpc': "2.0", 'method': "call",
//                "params": {employee_task_id,employee_id,old_employee_id,task_changing_reason,employee_project_id,project_value,task_value,stage_id}
//            }),
//            success: function (message) {
//               console.log(message);
//              $('#show_popup').modal('hide');
//        },
//            error: function (data) {
//                alert("Error" + data)
//            }
//        });
//   }
//};
//function assignallFunction() {
//
//    var old_employee_id = document.getElementById('old_employee_id').value;
//    var stage_id = document.getElementById('stage_id').value;
//    var task_changing_reason = document.getElementById('task_changing_reason').value;
//    var select_employee_task = document.getElementById('employee_task');
//    var employee_task_id = select_employee_task.options[select_employee_task.selectedIndex].value;
//    var selected_employee = document.getElementById('all_employees');
//    var employee_id = selected_employee.options[selected_employee.selectedIndex].value;
//    var getResultTask = document.getElementById("myCheckTask");
//    var getResultProject = document.getElementById("myCheckProject");
//    var task_value=getResultTask.value;
//    var project_value=getResultProject.value;
//    var select_employee_task = document.getElementById('employee_task');
//    var select_employee_project = document.getElementById('employee_projects');
//    var employee_project_id = select_employee_project.options[select_employee_project.selectedIndex].value;
//    var employee_task_id = select_employee_task.options[select_employee_task.selectedIndex].value;
//    if (task_changing_reason == ''){
//        alert('Please Add a Reason');
//        document.getElementById("task_changing_reason").focus();
//    }
//    else{
//        $.ajax({
//            type: "POST",
//            dataType: 'json',
//            url: '/assign/all/task/',
//            contentType: "application/json; charset=utf-8",
//            data: JSON.stringify({
//                'jsonrpc': "2.0", 'method': "call",
//                "params": { employee_task_id,employee_id,old_employee_id,task_changing_reason,stage_id,employee_project_id,project_value,task_value}
//            }),
//            success: function (message) {
//               console.log(message);
//              $('#show_popup').modal('hide');
//        },
//            error: function (data) {
//                alert("Error" + data)
//            }
//        });
//   }
//};