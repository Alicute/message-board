 $(document).ready(function() {
                $('#message-input').focus();
                console.log(messages)
     function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 1500); // 3秒后隐藏Toast提示
}

                function renderMessages(messages) {
                $('#messages-container tbody').empty();
                messages.forEach((message) => {
                    $('#messages-container tbody').prepend(
                        `<tr data-id="${message.id}">
                            <td ><input type="checkbox" name="select-message" value="${message.id}"></td>
                            <td>${message.id}</td>
                            <td class="content-style">${message.content}</td>
                             <td>${message.time}</td>
                            <td>
                                <button class="normal-btn" onclick="editMessage(${message.id})">编辑</button>
                                <button class="normal-btn" onclick="deleteMessage(${message.id})">删除</button>
                                <button class="normal-btn" onclick="copyMessage(${message.id})">复制</button>
                            </td>
                        </tr>`
                    );
                });
            }
                 // 渲染消息
            if (messages) {
                renderMessages(messages);
            }

            $('#submit-btn').click(function() {
                const content = $('#message-input').val();
                if (content) {
                    $.ajax({
                        url: '/add_message',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({content:content}),
                        success: function(data) {
                            $('#message-input').val('');

                            renderMessages(data.messages);
                            showToast('提交成功！');
                                                        $('#message-input').focus();
                        }
                    });
                } else {
                                                $('#message-input').focus();
                }
            }
            );


            $('#delete-selected-btn').click(function() {
                const selectedIds = [];
                $('input[name="select-message"]:checked').each(function() {
                    selectedIds.push($(this).val());
                });

                if (selectedIds.length > 0) {
                    $.ajax({
                        url: '/delete_selected_messages',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ ids: selectedIds }),
                        success: function(data) {
                            renderMessages(data.messages);
                        }
                    });
                }
            });

            $('#select-all').click(function() {
                $('input[name="select-message"]').prop('checked', this.checked);
            });



            window.editMessage = function(id) {
                const newContent = prompt("Edit your message:");
                if (newContent) {
                    $.ajax({
                        url: '/edit_message',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ id: id, content: newContent }),
                        success: function(data) {
                            renderMessages(data.messages);
                            showToast('编辑成功！');
                        }
                    });
                }
            };

            window.deleteMessage = function(id) {
                $.ajax({
                    url: '/delete_message',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: id }),
                    success: function(data) {
                        renderMessages(data.messages);
                                showToast('删除成功！');
                    }
                });
            };

            // window.copyMessage = function(id) {
            //     const message = $(`tr[data-id="${id}"] td:nth-child(3)`).text().trim();
            //     console.log("```````",message)
            //     navigator.clipboard.writeText(message);
            //     alert('Message copied to clipboard');
            // };

            window.copyMessage = function(id) {
        const message = $(`tr[data-id="${id}"] td:nth-child(3)`).text().trim();
        navigator.clipboard.writeText(message);
        showToast('复制成功！');
}

        });