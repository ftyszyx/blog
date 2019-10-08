package main

import (
	"crypto/md5"
	"encoding/base64"
	"strings"
	"fmt" )


//data={"OrderCode":"","WaybillCode":"118954907573"}encrypt=urlformat=jsonmethod=querytracepartnerid=1266103timestamp=1498476554version=1.0pfb156zldvNJ0nll
func main() {
	data:="data={\"OrderCode\":\"\",\"WaybillCode\":\"118954907573\"}encrypt=urlformat=jsonmethod=querytracepartnerid=1266103timestamp=1498476554version=1.0pfb156zldvNJ0nll"
	fmt.Println(GetStrMD5(data))
}

func GetStrMD5(src string) string {
	return GetByteMD5([]byte(src))
}

//128bit   16字节 16*8  每个字节8bit可以表示256个信息
//每个字节可以存两个16进制的数字
func GetByteMD5(src []byte) string {
	cipherStr := md5.Sum(src)
	var codestr []byte
	for _,item:=range cipherStr{
		codestr=append(codestr,item)
	}
	ignsstr := strings.ToLower(base64.StdEncoding.EncodeToString(codestr))
	
	//md5str1 := fmt.Sprintf("%s", cipherStr) //将[]byte转成16进制
	return ignsstr

}