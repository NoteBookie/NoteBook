## 使用方法
---

###xiami.py（自动签到）
1. 修改你的个人信息

        data = {
        #change your information here
        'email' : '' ,
        'password' : '' ,
        'LoginButton' : '登 录'
        }
2. 执行

        python xiami.py
        >>> Start Login...
        Login Success!
        Success! You have signed in 2 days[already]
        >>>

###xget.py
1. 需求curl，请自行下载合适版本并丢在同目录下。
2. 不保证linux下可跑，可以作为借鉴。（其实修改\为/后应该就可以了）
3. 执行

        python xget.py -h
        python xget.py -s [songID] //下载单曲
        python xget.py -a [albumID] //下载专辑
        python xget.py -l [listID] //下载精选集
        
4. 暂时不能下载高品质音乐，并且下载「我的喜爱」正在以水磨工夫码出中（让我享受灿烂寒假）

以上。
        




