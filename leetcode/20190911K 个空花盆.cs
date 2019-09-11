using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


/*
K 个空花盆

花园里有 N 个花盆，每个花盆里都有一朵花。这 N 朵花会在 N 天内依次开放，每天有且仅有一朵花会开放并且会一直盛开下去。
给定一个数组 flowers 包含从 1 到 N 的数字，每个数字表示在那一天开放的花所在的花盆编号。
例如， flowers[i] = x 表示在第 i 天盛开的花在第 x 个花盆中，i 和 x 都在 1 到 N 的范围内。
给你一个整数 k，请你输出在哪一天恰好有两朵盛开的花，他们中间间隔了 k 朵花并且都没有开放。
如果不存在，输出 -1。
输入: 
flowers: [1,3,2]
k: 1
输出: 2
解释: 在第二天，第一朵和第三朵花都盛开了。
*/
namespace test
{
    class Program
    {
        //重复子串
        static void Main(string[] args)
        { 
            Console.WriteLine("a:{0}", KEmptySlots(new int[] { 3,9,2,8,1,6,10,5,4,7 },1));
            Console.WriteLine("ok");
        }

        public static int KEmptySlots(int[] flower, int K)
        {
            var openday = new int[flower.Length];
            for (int i = 0; i < flower.Length; i++)
            {
                openday[flower[i]-1] = i+1;
            }

            var right = K + 1;
            var okday = -1;
            for(int left=0;right< flower.Length; left++)
            {
                var nowday = Math.Max(openday[left], openday[right]);
                var ok = true;
                for (int i = left+1; i < right; i++)
                {
                    if (openday[i] <= nowday)
                    {
                        //不符合
                        ok=false;
                        break;
                    }
                }
                if(ok)
                {
                    if(okday==-1||nowday<okday)
                        okday = nowday;
                } 
                 right++;  
            }
           
            return okday;
        }

    }
}
