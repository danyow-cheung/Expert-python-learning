import opengl 

class Lazy_class_attribute(object):
    def __init__(self,function):
        self.fget = function 
    def __get__(self,obj,cls):
        value = self.fget(obj or cls)
        setattr(cls,self.fget.__name__,value)
        return value

class ObjectUsingShaderProgram(object):
    # trivial pass-through vertex shader implementation
    VERTEX_CODE = """
        #version 330 core
        layout(location = 0) in vec4 vertexPosition;
        void main(){
            gl_Position =  vertexPosition;
        }
    """
    # trivial fragment shader that results in everything 
    # drawn with white color 
    FRAGMENT_CODE = """
        #version 330 core
        out lowp vec4 out_color;
        void main(){
            out_color = vec4(1, 1, 1, 1);
        }
    """
    @Lazy_class_attribute
    def shader_program(self):
        print("Compiling")
        return opengl.shader
    