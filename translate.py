# coding=utf-8
import requests
import json
import execjs  # 用来执行js脚本
import time
import urllib.parse


class Py4Js:
    def __init__(self):
        self.ctx = execjs.compile(""" 
    function TL(a) { 
    var k = ""; 
    var b = 406644; 
    var b1 = 3293161072;       
    var jd = "."; 
    var $b = "+-a^+6"; 
    var Zb = "+-3^+b+-f";    
    for (var e = [], f = 0, g = 0; g < a.length; g++) { 
        var m = a.charCodeAt(g); 
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
        e[f++] = m >> 18 | 240, 
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
        e[f++] = m >> 6 & 63 | 128), 
        e[f++] = m & 63 | 128) 
    } 
    a = b; 
    for (f = 0; f < e.length; f++) a += e[f], 
    a = RL(a, $b); 
    a = RL(a, Zb); 
    a ^= b1 || 0; 
    0 > a && (a = (a & 2147483647) + 2147483648); 
    a %= 1E6; 
    return a.toString() + jd + (a ^ b) 
  };      
  function RL(a, b) { 
    var t = "a"; 
    var Yb = "+"; 
    for (var c = 0; c < b.length - 2; c += 3) { 
        var d = b.charAt(c + 2), 
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
    } 
    return a 
  } 
 """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


class google_translate:
    def __init__(self):
        self.js = Py4Js()


    def buildUrl(self, text, tk):
        value = {
            'client': 't',
            'sl': 'auto',
            'tl': 'zh-CN',
            'hl': 'zh-CN',
            'dt': 'at',
            'dt': 'bd',
            'dt': 'ex',
            'dt': 'ld',
            'dt': 'md',
            'dt': 'qca',
            'dt': 'rw',
            'dt': 'rm',
            'dt': 'ss',
            'dt': 't',
            'ie': 'UTF-8',
            'oe': 'UTF-8',
            'pc': '1',
            'otf': '1',
            'ssel': '0',
            'tsel': '0',
            'kc': '2',
            'tk': tk,
            'q': text
        }

        baseUrl = 'https://translate.google.cn/translate_a/single?' + urllib.parse.urlencode(value)

        return baseUrl

    def translate(self, text):
        text = text.replace('\n', '')
        url = self.buildUrl(text, self.js.getTk(text))
        res = text
        try:
            headers = {
                'accept': '* / *',
                'accept-encoding': 'gzip,deflate,br',
                'accept-language': 'zh-CN, zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'referer': 'https://translate.google.cn/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            }
            r = requests.get(url, headers=headers)
            time.sleep(0.3)
            result = json.loads(r.text)
            if result[7] != None:
                # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
                try:
                    correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                    correctUrl = self.buildUrl(correctText, self.js.getTk(correctText))
                    correctR = requests.get(correctUrl)
                    newResult = json.loads(correctR.text)
                    res = newResult[0]

                except Exception as e:
                    res = result[0]
            else:
                res = result[0]
            trans_data = [i[0] for i in res if i[0]]
            res = '\n'.join(trans_data)
        except Exception as e:
            import traceback
            print(url)
            print("翻译" + text + "失败")
            print("错误信息:")
            traceback.print_exc()
        finally:
            return res

if __name__ == '__main__':
    train_translate = '''
    (2) is trivial, computing some x- and y-coordinate distances up to some error tolerance. (1) involves parameterizing the ray and checking one of four inequalities. If the bottom left of the rectangle is ![](https://s0.wp.com/latex.php?latex=%28x_1%2C+y_1%29&bg=ffffff&fg=36312d&s=0)
 and the top right is ![](https://s0.wp.com/latex.php?latex=%28x_2%2C+y_2%29&bg=ffffff&fg=36312d&s=0)
 and the ray is written as ![](https://s0.wp.com/latex.php?latex=%5C%7B+%28c_1+%2B+t+v_1%2C+c_2+%2B+t+v_2%29+%5Cmid+t+%3E+0+%5C%7D&bg=ffffff&fg=36312d&s=0)
, thenâ€”with some elbow greaseâ€”the following four equations provide all possibilities, with some special cases for vertical or horizontal rays:

    '''
    trans = google_translate()
    res = trans.translate(train_translate)
    print(res)