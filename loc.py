from selenium.webdriver.common.by import By


class Locators:
    # +menu
    add_menu_loc = (By.XPATH, '//*[@id="root"]/div/div/div/div/div[1]/div/img')
    # Menu drop-down box to add friends
    add_friend_loc = (By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/div')
    # Enter friend account box
    add_input_account_loc = (By.CSS_SELECTOR, 'input.ant-input.ant-input-outlined')
    # confirm
    add_input_confirm_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.px-6')
# mx-2.flex.cursor-pointer.items-center.rounded-md.p-3:nth-of-type(1)
    # Profile”add friend“
    add_friend_info_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1:nth-of-type(1)')
    # Profile "Send Message"
    send_strange_info_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1:nth-of-type(2)')
    # Send verification content to friend
    send_info_loc = (
    By.CSS_SELECTOR, 'textarea.ant-input.css-1f72xif')
    # Confirm sending
    end_confirm_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.flex-1')
    tip_msg_loc = (By.XPATH, '/html/body/div[4]/div/div/div/div')

    # input box for sending messages
    msg_input_loc = (By.CSS_SELECTOR, 'div.ck-content.ck-editor__editable p')
    # message button
    send_msg_btn_loc = (By.CSS_SELECTOR, 'button.ant-btn.ant-btn-primary.ant-btn-compact-item'
                                         '.ant-btn-compact-first-item')

    # Message box after sending message
    msg_panel_loc = (By.CSS_SELECTOR, 'div._bubble_1t138_10')

    # Message box to receive messages
    received_panel_loc = (By.CSS_SELECTOR, '._message-container_1t138_1:not(._message-container-sender_1t138_21)'
                                           ' ._bubble_1t138_10')

    # used for  send pictures and video files ,this input
    # 用于选择文件的input元素定位器模板
    # file_input_locator = (By.CSS_SELECTOR, 'input[type="file"]')
    # image_upload_input_loc = (By.CSS_SELECTOR,'input[type="file"]')
    file_type_to_loc = {
        'image': (By.CSS_SELECTOR, 'input[type="file"][accept="image/*"]'),
        'video': (By.CSS_SELECTOR, 'input[type="file"][accept=".mp4"]'),
        'file': (By.CSS_SELECTOR, 'input[type="file"][accept="*"]')
    }
    file_sent_success_loc = {
        'image': (By.CSS_SELECTOR, 'img[src*="msg_picture"]'),
        'video': (By.CSS_SELECTOR, 'img[src*="msg_videoSnapshot"]'),
        'file': (By.CSS_SELECTOR, '  div > div > span > div.ant-spin-nested-loading.css-1f72xif > div >'
                                  ' div > div.mr-2.flex.h-full.flex-1.flex-col.justify-between.overflow-hidden')
        # 'file': (By.CSS_SELECTOR, 'img[src*="http://192.168.2.20:10002/object/8745629711/'
        #                        'msg_videoSnapshot_2c4a488a52392039d47696c6d3853e8d.png"]')
    }


    # Specify picture
    # img1 = (By.CSS_SELECTOR, 'img[src*="http://192.168.2.20:10002/'
    #                          'object/8745629711/msg_picture_55bdf4cb39e3c472bb1be6c56581f237.png"]')
    img1 = (By.XPATH, ' // *[ @ id = "chat_b37eb95cdee1324548c48a9f99143688"] / '
                             'div / div / span / div[1] / div / div / div')

    # Specify video
    # video1 = (By.CSS_SELECTOR, 'img[src*="http://192.168.2.20:10002/object/8745629711/'
    #                            'msg_videoSnapshot_2c4a488a52392039d47696c6d3853e8d.png"]')
    video1 = (By.XPATH, '// *[ @ id = "chat_0b2e2511e2ec2f5dd31e36d727ab9c3b"] / '
                               'div / div / span / div[1] / div / div / div[1] / img')

    # Specify file
    # '#chat_cee4930d6393aa93019c08971044355f > div > div > span > div.ant-spin-nested-loading.css-1eammq7 > div > div')
    # //div[@class="ant-spin-container"]/div/div/div[contains(text(),"OpenIM.pdf")]
    file1 = (By.XPATH, '//div[@class="ant-spin-container"]/div/div/div[contains(text(),"OpenIM.pdf")]')

    # Agree with friends
    contacts = (By.CSS_SELECTOR, '#root > div > div > div > div > div.ant-layout.ant-layout-has-sider'
                                 '.css-1f72xif > aside > div > div > span:nth-child(3) > div > div')
    # New friend request
    newFriend_list = (By.CSS_SELECTOR, 'li.mx-2.flex.cursor-pointer.items-center.rounded-md.p-3:nth-of-type(1)')

    # agree
    agree = (By.CSS_SELECTOR, 'button.ant-btn.css-1f72xif.ant-btn-primary.ant-btn-sm')
