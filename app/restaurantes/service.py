import base64
from django.core.files.base import ContentFile


def upload_banner(evento, request):

    dados = {'sucesso': False, 'code': 500}

    image_data = request.data.get('banner')
    
    try:
        format, imgstr = image_data.split(';base64,')
    except:
        dados['mensagem'] = "Formato inválido"
        return dados

    ext = format.split('/')[-1]
    
    if ext not in ['jpg', 'jpeg', 'png', ]:
        dados['mensagem'] = u"Formato inválido"
        return dados
    
    data = ContentFile(base64.b64decode(imgstr))  
    file_name = "{0}.{1}".format(evento.uuid, ext)

    evento.banner.save(file_name, data, save=True)
    dados['sucesso'] = True
    dados['code'] = 200
    
    return dados

     

