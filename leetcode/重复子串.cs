using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/*
给定两个字符串 A 和 B, 寻找重复叠加字符串A的最小次数，使得字符串B成为叠加后的字符串A的子串，如果不存在则返回 -1。

举个例子，A = "abcd"，B = "cdabcdab"。

答案为 3， 因为 A 重复叠加三遍后为 “abcdabcdabcd”，此时 B 是其子串；A 重复叠加两遍后为"abcdabcd"，B 并不是其子串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/repeated-string-match
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
*/
namespace test
{
    class Program
    {
        //重复子串
        static void Main(string[] args)
        {
            Console.WriteLine("a:{0}", RepeatedStringMatch("a", "aa"));
        }
         
        public static int RepeatedStringMatch(string A, string B)
        {

            var count = 1;
            string newstr = A;
            while (true)
            {
                if (newstr.Length >= B.Length)
                    break;
                count++;
                newstr += A;
            }
            if (newstr.IndexOf(B, 0) > -1)
            {
                return count;
            }
            else
            {
                newstr += A;
                if (newstr.IndexOf(B, 0) > -1)
                {
                    return count+1;
                }
            }
            return -1;
        }
         
    }
}
