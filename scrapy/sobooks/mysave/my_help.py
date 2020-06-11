import re
def is_number(str):
    try:
        # 因为使用float有一个例外是'NaN'
        if str=='NaN':
            return False
        int(str)
        return True
    except ValueError:
        return False

def clearComment(text):
    find_res = re.findall(r'//[^\n]*', text)
    if len(find_res) > 0:
        for item in find_res:
            text = text.replace(item, "//")
    return text

def getPostJson(text):
    find_res = re.search(r'data \:[^{}]*(\{[^}]*\})', text)
    postdata_str = find_res.group(1)
    postdata = getDictFromJson(text, postdata_str)
    return postdata

def getDataValue(text):
    find_res = re.search(r'data[\s]*\:[\s]*\'([^,}]*)\'', text)
    postdata_str = find_res.group(1)
    return postdata_str

def getJsValue(text,key):
    regex= re.compile(r"%s[\s]*=[\s]*(\'*[^;\'\}\&\;\,]*\'*)" % (key))
    find_res = re.search(regex, text)
    if find_res is None:
        #print("key not find:",key,text)
        return ""
    valuetext=find_res.group(1)
    if valuetext.startswith("'")==False:
        if (is_number(valuetext)):
            return int(valuetext)
        else:
            return valuetext
    return str(valuetext.replace("'",""))


def getDictFromJson(html,json):
    data={}
    find_res = re.findall(r'\'([^,\'\}]*)\':(\'*[^\',\}]*\'*)', json)
    for item in find_res:
        key_str=item[0]
        value_str=item[1]
        if value_str.startswith("'")==False:
            if(is_number(item[1])):
                data[key_str]=int(value_str)
            else:
                data[key_str] = getJsValue(html,value_str)
        else:
            data[key_str]=value_str.replace("'","")
    return data

def newError(msg="",data={}):
    if msg=="":
        return {'errno': 0, "msg":msg,"data":data}
    else:
        return {'errno': 1, "msg": msg, "data": data}

def newSuccess():
    return {'errno': 0, "msg": "", "data": {}}