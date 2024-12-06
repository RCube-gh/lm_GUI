import flet as ft
import sys
from gpt4all import GPT4All
import os

md_text = """
### Your Chat Here!!
"""

def main(page: ft.Page):
    page.title="Chat CPT"
    page.window.height=750
    page.window.width=550
    page.window.resizable=False
    page.update()
    page.vertical_alignment=ft.MainAxisAlignment.CENTER

    def text_submit(e):
        global md_text
        print("text_submitted")
        user_input_text=text_box.value
        text_box.value=""
        md_text=md_text+'You> '+user_input_text+'\n\n'
        chat_text.value=md_text
        page.update()
        output=model.generate(user_input_text)
        md_text=md_text+'AI> '+output+'\n\n'
        chat_text.value=md_text
        chat_container.content.append(ft.Text('aaaaaaaaa'))
        page.update()

    def on_keyboard(e:ft.KeyboardEvent):
        if e.ctrl and e.key=="Enter":
            text_submit(e)
        if e.key=="Escape":
            page.window.destroy()
            sys.exit()
        page.update()

    def select_model_path():
        page.open(model_path_modal)
        if os.path.isfile('model_path.txt'):
            with open('model_path.txt','r') as f:
                path_input.value=f.read()
                page.update()

    def create_model():
        global model
        model_path=""
        with open('model_path.txt','r') as f:
            model_path=f.read().rstrip('\n')
            dir_path,filename=os.path.split(model_path)
        model=GPT4All(model_name=filename,model_path=dir_path,allow_download=False)
            
    def handle_close(e):
        page.close(model_path_modal)
        with open('model_path.txt','w') as f:
            f.write(path_input.value)

    page.on_keyboard_event=on_keyboard

    path_input=ft.TextField(label='path')

    model_path_modal=ft.AlertDialog(
            modal=True,
            title=ft.Text('Enter the absolute path to your model'),
            content=path_input,
            shape=ft.RoundedRectangleBorder(radius=6.0),
            bgcolor='#222222',
            actions=[
                ft.TextButton('OK',on_click=handle_close),
                ],
            )

    title_text=ft.Text("ChatCPT",size=30)
    model_path_button=ft.FilledButton(text='Model Path',bgcolor='#333333',color='#DDDDDD',on_click=lambda e: select_model_path())
    chat_text=ft.Markdown(md_text,selectable=True,extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,on_tap_link=lambda e: page.launch_url(e.data),)
    text_box=ft.TextField(label="Enter Text",width=400,multiline=True,max_lines=3,border_color='#a9a9a9')


    title_container=ft.Container(
            content=title_text,
            alignment=ft.alignment.center,
            )
    model_path_button_container=ft.Container(
            content=model_path_button,
            alignment=ft.alignment.top_right,
            )
    chat_container=ft.Container(
            content=chat_text,
            alignment=ft.alignment.top_left,
            width=500,
            height=500,
            border_radius=10,
            )
    input_fields=ft.Row(
                [
                    text_box,
                    ft.ElevatedButton(text="Submit",on_click=text_submit)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

    page.scroll="auto"
    page.add(
        title_container,
        model_path_button_container,
        chat_container,
        input_fields
    )
    text_box.focus()

    if not os.path.isfile('model_path.txt'):
        select_model_path()
    if os.path.isfile('model_path.txt'):
        create_model()

ft.app(target=main)
