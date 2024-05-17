from selenium.webdriver.common.by import By


class Locators:
    # +菜单
    add_menu_loc = (By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div/img')
    # 菜单下拉框添加好友
    add_friend_loc = (By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/div')
    # 输入好友账号框
    add_input_account_loc = (By.CSS_SELECTOR, 'input.ant-input.ant-input-outlined')
    # 确认
    add_input_confirm_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.px-6')

    # 个人资料”添加好友“
    add_friend_info_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1:nth-of-type(1)')
    # 个人资料"发消息"
    send_strange_info_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1:nth-of-type(2)')
    # 发送好友验证内容
    send_info_loc = (
    By.CSS_SELECTOR, 'textarea.ant-input.css-1eammq7')
    # 确认发送
    end_confirm_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1')
    tip_msg_loc = (By.XPATH, '/html/body/div[4]/div/div/div/div')

    # 发消息的input输入框
    msg_input_loc = (By.CSS_SELECTOR, 'div.ck-content.ck-editor__editable p')
    # 确认发消息的按钮
    send_msg_btn_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-compact-item'
                                         '.ant-btn-compact-first-item')

    # 发送消息后的消息框
    msg_panel_loc = (By.CSS_SELECTOR, 'div._bubble_1t138_10')

    # 接收消息的消息框
    received_panel_loc = (By.CSS_SELECTOR, '._message-container_1t138_1:not(._message-container-sender_1t138_21)'
                                           ' ._bubble_1t138_10')

    # 发送图片loc
    # 用于选择文件的input元素定位器模板
    file_input_locator = (By.CSS_SELECTOR, 'input[type="file"]')
    # image_upload_input_loc = (By.CSS_SELECTOR,'input[type="file"]')

