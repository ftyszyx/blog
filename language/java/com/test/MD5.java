package com.test;  
  
import java.io.UnsupportedEncodingException;  
import java.security.MessageDigest;  
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

import sun.misc.BASE64Encoder;  
  
public class MD5{   
  
    public static final String Md(String plainText,boolean judgeMD) {   
        StringBuffer buf = new StringBuffer("");   
        try {   
        MessageDigest md = MessageDigest.getInstance("MD5");   
        md.update(plainText.getBytes());   
        byte b[] = md.digest();   
        System.out.println("len: " + b.length);
        int i;   
        for (int offset = 0; offset < b.length; offset++) {   
            i = b[offset];   
            if(i<0) i+= 256;   
            if(i<16)   
            buf.append("0");   
            buf.append(Integer.toHexString(i));   
        }   
      System.out.println("32result: " + buf.toString());
      System.out.println("16result: " + buf.toString().substring(8,24));  
  
        } catch (NoSuchAlgorithmException e) {   
        // TODO Auto-generated catch block   
        e.printStackTrace();   
        }   
        if(judgeMD == true){  
            return buf.toString();  
        }else{  
            return buf.toString().substring(8,24);  
        }  
          
    }   
    public static final String EncoderPwdByMd5(String str) throws NoSuchAlgorithmException, UnsupportedEncodingException {  

        MessageDigest md5 = MessageDigest.getInstance("MD5");  
        BASE64Encoder base64en = new BASE64Encoder();   
        //String newstr = base64en.encode(md5.digest(str.getBytes("utf-8")));   
        //byte[] arr=md5.digest(str.getBytes("utf-8"));

        /*
        System.out.println("newstr: " +arr.length );   
        System.out.printf("newstr: :%s\n" ,arr );   
        System.out.printf("newstr: :%s\n" ,arr ); 
        System.out.printf("newstr:%s\n",arr );   
        System.out.println("newstr: " + newstr);    
        */
        md5.update(str.getBytes());
        byte[] m=md5.digest();
        return base64en.encode(m);  
    }  
//????   
    public static void main(String[] args) {   
        System.out.println("Hello, world!");
        //String data="data={\"OrderCode\":\"\",\"WaybillCode\":\"118954907573\"}encrypt=urlformat=jsonmethod=querytracepartnerid=1266103timestamp=1498476554version=1.0pfb156zldvNJ0nll";
        String data="data={\"OrderCode\":\"\",\"WaybillCode\":\"AB62512456AU\"}encrypt=urlformat=jsonmethod=querytracepartnerid=1261885timestamp=1569470286version=1.0pfb156zldvNJ0nll";
        Md(data, true);   
        try {  
            System.out.println("result: " + EncoderPwdByMd5(data));  
        } catch (NoSuchAlgorithmException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        } catch (UnsupportedEncodingException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
}  