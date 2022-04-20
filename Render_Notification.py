import bpy
import bpy.app.handlers
from bpy.app.handlers import persistent


import smtplib , ssl
from email.message import EmailMessage

#Send an email Notification once a render is finished


bl_info = {
    "name" : "Render notification Mail service",
    "blender": (2, 93, 0),
    "category": "Render",
    "author": "Abdullah, Taqiedin",
    "description": "Sends an email when your render is finished."
}





class input_operator(bpy.types.Panel):
    bl_label = "Render notification Mail service"
    bl_idname = "OBJECT_PT_Render_notification"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_catagory = "input tool"

    def draw(self, context):
        layout = self.layout


        row = layout.row()
        row.operator("wm.textop")



class WM_OT_TextOp(bpy.types.Operator):
    bl_label = "Render notification text operator"
    bl_idname = "wm.textop"    
    
    
    
    email : bpy.props.StringProperty(name= "Enter Email:")
    password : bpy.props.StringProperty(name= "Enter Password:",subtype='PASSWORD')


    def execute(self,context):
        
        bpy.types.Scene.email = self.email
        bpy.types.Scene.password = self.password


        return {'FINISHED'}

    def invoke(self,context, event):
        return context.window_manager.invoke_props_dialog(self)






@persistent
def send_mail(scene,y):


    email_user = bpy.context.scene.email                  
    email_password = bpy.context.scene.password  



    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    print("'" +filename+"'") 
    text = " has finished rendering."
    content = filename + text
    
    

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "Render complete!"
    msg["From"] = email_user
    msg["To"] = email_user

    context=ssl.create_default_context()

    #
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context = context)
        smtp.login(msg["From"], email_password)
        
        try:
            smtp.send_message(msg)
            print("------------------------------------------")
            print("Render complete")
            print("mail Sent successfully")
            print("------------------------------------------")
            
        except:
            print("------------------------------------------")
            print("failed to send mail")
            print("------------------------------------------")
            

        smtp.quit()    


#WM_OT_TextOp
def register():
    
    bpy.utils.register_class(WM_OT_TextOp)
    bpy.utils.register_class(input_operator)
    bpy.app.handlers.render_complete.append(send_mail)

def unregister():
    bpy.utils.unregister_class(input_operator)
    bpy.utils.unregister_class(WM_OT_TextOp)
    bpy.app.handlers.render_complete.remove(send_mail)





if __name__ == "__main__":
    register()
