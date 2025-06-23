document.addEventListener('DOMContentLoaded', function() {
    const avatarUploadInput = document.getElementById('id_avatar_upload'); // 实际的文件输入框
    const avatarPreviewImg = document.getElementById('avatar-preview'); // 预览头像的 img 标签
    const fileUploadText = document.querySelector('.file-upload-text'); // “点击头像更换”的文本提示

    if (avatarUploadInput && avatarPreviewImg) {
        // 1. 点击头像图片时，触发文件输入框的点击事件
        avatarPreviewImg.addEventListener('click', function() {
            avatarUploadInput.click();
        });


        // 2. 文件输入框内容改变时，更新预览图
        avatarUploadInput.addEventListener('change', function(event) {
            const file = event.target.files[0]; // 获取用户选择的第一个文件

            if (file) {
                const reader = new FileReader(); // 创建 FileReader 对象

                reader.onload = function(e) {
                    // 文件读取完成后，将结果 (Data URL) 设置为预览图片的 src
                    avatarPreviewImg.src = e.target.result;
                };

                // 读取文件内容为 Data URL (Base64 编码的图片数据)
                reader.readAsDataURL(file);
            } else {
                // 如果用户取消了文件选择，保持当前预览图不变
                // （无需操作）
            }
        });
    }
});