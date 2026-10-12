# 文字记录：user guides代码相关内容分享 2026年10月10日

> 会议主题：user guides代码相关内容分享  
> 会议时间：2026年10月10日（周六） 14:31 - 15:03 （GMT+08）  
> 智能纪要：[user guides代码相关内容分享 2026年10月10日](https://zilliverse.feishu.cn/docx/D6zidlbaTo6DfYxdnleceiUtnlX)



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:00:42  
喂。好。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:00:44  
m 老师，能听见吗？你可以共享一下吗？或者给我们讲讲你刚才贴的那个 Skill 的目录。这个，啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:00:59  
其实没什么，这个也我也不用共享，因为我在那群里面，你看我该我该敲出来那个子动，他会去自己去做的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:01:08  
那你是怎么做的，也可以跟我们说说。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:01:12  
这样，它是一个那个后台。是一个服务的，然后后面，就是会有很多个这种类似于这种子的 agent 这种东西，然后我发一个指令的话，它就会去创建一个这种子的 agent。然后去引用这个文档，然后去更新。他更新可能是用到了那个飞书的那些 API 之类的东西，然后你还需要再这个机器上去把，就相当于我是把我的飞书账号用来给他。授权给他，让他去改这文档，对吧？然后他就能访问了，访问了也能去改。然后这个，然后那个 skill 呢，就是我定了一组 skill， 就是你点开那个我给的那个 Github 那个什么没有什么 skills 那个东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:01:57  
嗯嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:01:57  
那里面有一个它是它用来是更新这种是飞书上的这个这种 user guide 文档，然后它里面会定义说用什么规则。然后每种语言去，具体怎么做？就每种语言有有自己的特性嘛。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:02:13  
我没有看到 skill 目录诶，有 skill。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:02:13  
然后，我之前在群里面发了那个就是有个叫 merge skills， 一个链接。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:02:25  
嗯。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:02:25  
我看到了。啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:02:26  
就那个是个 GitHub 的 libra， 里面全是一堆 skill 的，每一个就是 master 的这种仓库，我就单独建了一个。然后这个是用来做这是个什么造型？



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:02:36  
就是这个，是吧？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:02:37  
这是跟里面做的事情，其实就是把这些 reaper 的这种内部的这种结构啊，然后它的这种设计啊、模式啊。就是全部描述一遍，让那个让那个 AI 去跑的时候，它就是不需要就读完一遍，就是相当于是比较快，能够大概知道在哪个地方去找这些东西。然后每个 SDK 基本都有都有一个专门的 skill。这个。当你去给这个机器人去，让它去浏览这文档的时候，它会自动，因为这 skill 已经，我已经装在那台机器上了，所以它能够加载所有的 skill。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:02  
对。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:03:12  
然后它可以就是根据你要更新的是哪一个 SDK 文档，或者是哪一种。反正7种中的任一种吧，然后他们就去找了这10个。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:21  
但是我看，就是我昨天看你那个。这样，我昨天看，就是我这边有那个你打开的文档的记录嘛。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:03:32  
对。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:33  
你稍等啊，在哪里？哦，这。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:03:35  
昨天一晚上跑了100多个，对吧？



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:35  
对。我就是看了你，就是好像，就你这个店小二和店小林，是店小林吗？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:03:43  
对。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:45  
对他，对他一直。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:03:45  
店小二做的。店小二是我一台机，这是两台机器，现在我给你是另外一台机器。就是他们其实是是一样的服务，就是店小二是跑在我这个工作机上的，然后店小二这个是跑在那个我找了一台，那个闲置的机器上的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:03:51  
啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:04:02  
然后这个他跑的时候，我昨天是这么跟他说的，你建一个那个后台的一个轮询，每分钟去就是我先让他把这个清单，就是把那个100多个那个飞书的那文档链接全部整合到一个 MD 文件里面去。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:04:02  
嗯。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:04:19  
嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:04:19  
那 MD 文件在我本地的，就是在这个服务的那个本地。然后跟他说这里面100多个链接，然后你去后台建个轮询，你去每分钟地去拿一条，然后给一个子 agent 去。让他去 review， 去更新，然后等那个，有闲置的那个 agent 来，我这里定的上线这个文档的这个 review 上限是4个吧。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:04:36  
嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:04:44  
就是同时并行4个4个任务，所以他可能4个都在忙，然后是跟他说，如果是有空闲的，你就给他，就一分钟轮询，不要太紧。然后他就会不断地去轮询，然后去，他就会一个个去发嘛，这些任务，要不然大概跑了130个吧。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:05:02  
嗯。对，我就是觉得你今天速度很快，你是通过轮询的方式让派，相当于派子 agent 去调那个 skill 往文档里填代码的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:05:05  
嗯，然后每对，因为他都是跑在同台机器上，他那 skill 是一样的，然后他的这个那个 skill 里面有说到怎么验证。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:05:16  
是吧？那你这些代码都是验证过的，是吧？相对于 Milvus 的机器来说。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:05:29  
就说如果我的提示语里面说要真实的运行的验证的话，它会真实去跑，而且要求那个服务上，那个机上有一个 milvus server。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:05:35  
嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:05:40  
这 milvus server 是我后台自己起的。如果没有起的话，他就不会做真实的验证，就是做不了。但他至少会做这种静态的检查，代码检查这类东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:05:50  
啊，对，就是做静态。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:05:52  
对于有些那种需要编译的，它也会编译的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:05:54  
啊。那，嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:05:56  
所以基本能保证那个片段那种正确性嘛，就是不会有什么太明显的这种错误。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:04  
对，我看你这些 skill 里面，我看一下。好像都是没有什么，就是他，因为我看你产出的那些 SDK 的那些文档，结构有一些不一样，然后有的时候他会，那种样式会。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:20  
嗯。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:21  
跟着不用一起跑，然后。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:26  
格式会漂移。叫，这种。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:30  
有时候做的不是特别准。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:32  
是的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:32  
我有时候是要看一下，我基本上后面要扫一遍的，就是他做完之后，有些他可能会漏的，像那个飞书妙记有一个他是做不了。有个事情他做不了，就是 session man.我们不是把那些片段都放了一个那个叫 sync source 里面嘛，就是在一个代码块里面。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:48  
同步快。对。同步快。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:51  
对，那个代码块它它 API， 飞书 API 是建不了的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:51  
嗯嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:54  
如果文档里面没有这个东西，它就没法加。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:06:54  
是的， API gem 的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:06:57  
所以他会直接就是漏过去了，所以得手动，就是我有时候得手动地加，就是我会让他去检查一遍，看哪些文档是没有这东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:00  
啊。但是我看你但是我看你改的这几篇里面，他们都是同步快呀，你好像加进去了。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:08  
现在就创建搜索会。所所以现在你这个。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:14  
现在不符合。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:14  
对，我这边也碰到同步。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:15  
红利。重新什么？对。那如果发生。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:18  
就是你这边，就是你，我在这个飞书上。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:22  
对，他那个过程也会做。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:22  
诶，等一下，我的飞书呢？就是这里，我看你点的这几块。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:26  
嗯。他不改。不改。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:29  
看也不是同步快啊。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:29  
你之前的入口会给到低嘛，我最低。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:31  
里面的代码。嗯。你加进来。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:33  
同步块，他如果有 sync source 的，可能肯定是我手动加的，或者是原来就有的，他是他是自己加不了，就他如果看见有有 sync source。他就会把那个我是进了代码官方。放进去，但如果没有的话，他就。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:46  
那你是怎么知道他没有加进去呢？



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:47  
我我发现各，我发现各组是。他就他就放不了。然后可能还是其他比如 miss。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:51  
我知道他放不了，就是你是怎么知道这一块他放不了？



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:53  
嗯。那你不可能，第三的只会。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:07:56  
然后你是有东西通知你吗？



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:58  
就是。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:07:59  
那也是让他去检查一遍，就是你刚才说，就是检查这文档里面的。就是代码块有没有被现在 source 包住的？没有包住的话就把它列出来，然后点进去看，然后看见确实是它就手动给加，这个是蛮费时间。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:15  
就是有的三月份先有了，三月份后有了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:16  
sync source 其实是可以看的，就是 sync source 它有 child， 它的 child 里面是可以看的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:21  
嗯。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:23  
我我我的我的点就是说，如果说我发布已经对齐融合发热这一套。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:24  
我给你看一下。SinSource 是能看。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:28  
机器人它没法。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:29  
然后数据这一套还需要。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:30  
看能看得到。我再想想。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:31  
他应该是没法改，是不是？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:35  
他没法加，就是没法加 sync source， 他可以给你加代码块，就是他，如果你没有 sync source， 他可以把代码块放到外面也可以。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:38  
啊。啊。啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:43  
但是我还我们最好是能放，都放在统一放在 salesforce 里面。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:48  
对对对对，就是这个问题。啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:08:51  
所以我这边都是手动的加新的 source， 然后让他把这个代码块放进去。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:08:56  
哦，相当于你给了他一篇文档，然后他扫一下这里面代码去补一些代码块，然后这些补的代码块可能不在 sync source 里面。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:01  
我。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:05  
然后你手动把它拖进去的。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:06  
对。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:07  
是这个意思。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:07  
啊，不不不，没没有，就是就是我在他更新之前，我就先把 sync source 做好了，就是把一个 sync source 放在那里。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:14  
啊。啊啊啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:16  
然后把那个就至少有个 Python 那代码块嘛，反正他 Python 代码块。丢在那个申诉里面，后面他就会后续的就会自己去加。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:22  
啊，啊，我懂了。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:24  
嗯。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:25  
就是你这个 house 也相当于是外面这个框框，你先建好了，然后里面有一块 Python 的，然后让他补其他的，是这个意思。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:25  
如果你没有。嗯。对。但是如果之前没有，然后他去更新了，就你没有手动的加，然后去更新了，他就会直接就平铺在那上面，所以后面我还得手动的把它那些加的那些东西代码会放进去。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:48  
啊，我明白了。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:49  
所以都是一样的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:50  
嗯嗯嗯。好的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:52  
主要在，飞书 API 不支持这个操作，所以这没办法。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:09:55  
然后我就接进去了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:09:56  
啊。我再看一下啊，那。就是那个还是关于这个 SDK 的文档写作啊，就我这边其实也弄了一套那个往飞书上写的那个 skill 吗？



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:10:04  
人员的不统一也不少，我觉得。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:10:08  
嗯。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:10:08  
新手包。先把华为。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:10:15  
然后我发现他每次产出都不是很。



说话人 2 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:10:15  
先把华为。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:10:20  
等一下啊。对，这个，就是我也弄了一套 skill。这里，就我这个 skill 里面就写这个 API reference 的，因为它每次往飞书上写，写出来的那个样子，就是有的时候是这个样子。有的时候是那个样子的，样式不一样。再就是有时候它一般不会缺那个不会缺参数，因为它都是扫的那个 SDK 里面做静态分析，然后拿到那些参数啊，然后签名啊。什么东西的，这些都应该都有。但是就是他可能样式上会有一些差异，有的时候他会写错地方。就后来我问了一下那个就用 SQL 去做了 agent， 做了一下调查。就里面他们说是加很多 harness， 如果你想让那个样式输出比较确定性的话，就要加一些 harness 检查。就是添加一些 fixture。然后添加一些 test 文件，去对你，他写好的那个文件做 test， 做了 test 之后发现， test 它里面有一些样式的漂移。然后就让返工，让 agent 去改，他就相当于也是一个 loop 的形式。我后来就在这里面补了这些东西，然后就是我现在等于往那个，我给你看一下。就是我为了同步你那个。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:11:57  
那这种就是用飞书的弊端了，它这个飞书里面的那个样式比那个复杂多了，比 MD 文件复杂多了，它有时候并不是很能准确地做这种事情。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:12:00  
对。是的，是的。对，我就，因为我这边要去，首先第一个是就是 zilliz 的文档都是从飞书上拉的，现在一时半会我也不可能很快地把它推掉。所以我现在是把你那个同步到飞书上，然后我就跑了这些东西，跑了这些战役，然后慢慢地把你的文档给同步过来，但是同步过来我发现 Rust 这边完全是新的嘛。因为我那边没有写过，所以我这个是准备做成就是以 webcontent 的里面的那个 webcontent 的你写的那些文档为主。然后我这边呢，会维护一套。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:12:49  
overlay， 就是在那个上面去定制 zlist 的文档。就比如说这一篇，如果两边是一样的，那这篇文档就直接用过来。如果这一篇和 zlist 的差异在于 zlist 有定制的参数。那我就在 overlay 里面去写 zlist 的参数，然后合并你那边，然后发到 zlist。然后再就是如果这个文档只有 zlist 有，比如说 volume 的那一套。那我就只在 zlist 这边写，你这边没有嘛，那就是我这边为主，所以就是大概是这样一套 overlay 的机制去发那个 zlist 的文档。因为现在就等于说是，您那边写完了之后，我需要做一次同步嘛，然后放 zlist 这边，还有您这边做代码的验证都是都是在 Milvus 上做的。那这 list 的 serverless。和 dedicated 的，还有我们的这种。集群上的差异，功能上的差异，虽然我能扫代码库扫出来一些，但是还是要验证一下，就是 Milvus 能跑， Zilliz 一定能跑吗？server， 那 Zilliz 能跑，是 Serverless 能跑，还是 Dedicated 能跑？所以这个也是要重新跑一下。就这样的话，暂时我们可以达到一个相对来说的一个平衡。所以后面我还是希望说去跑一下，在 zlist 上跑一下您这边添加的代码。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:14:18  
这个事情我会交给李鋆去做，然后后面李鋆可能会有一些问题，如果碰，他在实施的过程中碰到一些问题，也麻烦您能够帮着帮着一起解决一下。看看，您看可以吗？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:14:32  
可以，就是我觉得吧，就是走飞书这一套的话，你会觉得越来越不方便的。其实我现在我可以做到说就如果只是，如果只是 Github 上的这些 MD 文件，我可以做到让我，我在 SDK 里面发一个 tag。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:14:38  
对，是的，我今天早上。我今天早上跟你。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:14:49  
就是发一个新版本的话，全部都是自动化的。这自动的发布，然后自动的写文档，自动的更新文档，所有东西全自动的，全部可以做到这这一步，然后你在飞书上是不可能做到的。这全很麻烦，你在飞书上。所以说以后你会越来越觉得很麻烦。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:15:04  
没有，就是。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:15:04  
我以后只要打一个 tag， 这时候做完所有事情了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:15:07  
不是，我跟你讲一下现在碰到什么什么样的问题啊，或者你也帮，可以帮我们讨论一下，就是我现在存在什么什么样的一些问题。我给您看一下。稍等。就是这个是 zilliz 的文档的仓库嘛，然后这个文档仓库里面，我们是每日自动构建，每日从飞书上拉取，每日推到 uat。



<cite type="user" uid-ref="u3" user-name="Leryn Li"></cite> 00:15:31  
我家里好像没有共享，现在还是那个127.0。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:15:33  
啊啊。好，这个是我们那个 zilliz 的仓库，这个是每天在自己构建的，然后他会从飞书上把文档拉下来，然后每天后面会把它安排到。推到，自动推到 UAT。嗯。然后这里面，因为我们文档存在什么问题呢？第一个问题是， Milvus 和 Zilliz 发布并不同步， Milvus 发了新功能，在 Zilliz 上也不见得马上就要上来。对吧？然后， zilliz 这边，于是我们就需要对这些内容做隐藏，然后发上来。这是做隐藏，那隐藏我们做了一些体系化的标签。去打这个隐藏的标签，去隐藏某些内容。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:16:20  
第二个就是我这里是文档在开发的过程中，我前面在开发的过程中，可能产品有个版本要上嘛，那我开发的时候，我会有一个会有一个 Next 的版本。然后上到 Prod 的是一个 Current 版本。但是我们现在等于诶，只允许打一个镜像，因为打两个镜像的话，其实没有办法保证这两个镜像，是有接续关系的，所以我们是打一个镜像。打一个镜像呢。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:16:51  
我在 UAT 上要显示我当前已经开发的内容，但是在 Prod 里面我要把这些内容给隐藏掉，所以我们有一个 current 和 next 的版本的一个关系。那也就是说我们有内容过滤的标签体系和版本过滤的标签体系。那这两个体系呢，我也 Milvus 这边是不存在这个问题的，就是你可以，上了什么内容，你可以发什么版本，对吧？但是 Zilliz 这边不行。因为我们要保证，就是，这个版本。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:17:26  
上了，然后我们相关的内容才能提供，没上之前是不提供的。那你 Milvus 那边，你可以保证它自动化就可以做到这一点，但是 Zilliz 跟 Milvus 之间还是有一个时间差的。那这个时间差我们要通过这些标签体系来表，来保证。那这些如果有了这些东西的话，我这边也是做到每日去构建，后面我跟李鋆今天早上也看了，然后李鋆也是觉得在飞书上维护其实是不可持续的。我认这个事情，但是我们如果要往 Markdown 上面去推的话。也，我这个方向我认，但是我们这种能力是不能缺失的，就是后面我还是希望我们能有这种控制的能力。就是内容控制的能力和版本控制的能力，让文档发出来，不会说文档发的比早于产品。或者是文档发的内容，实际上还没有。产品还没有 ready， 这种，所以是的，是没有关，但是因为。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:18:28  
其实我觉得你说的这种过滤这种事情，其实跟走不走飞书是没有关系的。我全走 Github 的 repo 一样的。只要有黑名单白名单够了，然后相当于你可以从那个 web- content 那边直接更新，往这个 zdoc 那边更新。不走飞书上。现在是先走飞书，然后再从飞书再走 zdoc。走了个三角形，就是本来一条边能走完的，然后现在走两条边，当然就麻烦了，你后面维护什么，这一套流程都很麻烦。就是过滤这事情，在哪、哪个、哪条路都可以走。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:18:58  
但是现在我，因为 web- content 不是，我明白你说的意思啊，就是我刚才说了，也是我说我认这个事情，就是你觉得两条边不好。一条边更快。这个事情我认，就后面我们也会朝这个方向去改，但是目前我没有办法很快的改到你说的那个事情，那个样子来。因为首先我们这边也没有那么快，上手也没有那么快，然后我们去改这些东西呢，也都是摸出来的。我做这些东西也都是一点一点摸出来，所以我是想往那个方向去改，但是改的过程中可能还会有一些问题，我们，还是想找你探讨一下。然后接着把这个事情给做顺，是这样。嗯，你说的这个事情就是从 web contents 往 zilliz 去改，然后共享的文档以 Milvus 为主，然后我们这边做定制嘛。我明白你的意思，是的。就是做定制的这个事情，这个机制我们这边来把握嘛，然后可能实施的过程中，也遇到什么问题，我们会跟你再探讨一下。是这样，后面会是直接往这个， Markdown 这个方式去转。因为为什么之前我们要往飞书上写？也是产品这边的要求。但是如果我们就想全自动去做这个事情，现在怎么说呢， Zilliz 这边就是自动的，其实我当时就是做这件事情的时候。就是以 Zilliz 这边为主， Milvus 那边是从 Zilliz 这边的一个相当于是一个副产品。那现在我们把这个关系理顺。以开源这边为主，然后 Zilliz 这边是建在它上面的一个 Overlay。然后这样的关系可能会更顺一点。所以。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:21:00  
就是你要在飞书上 review 这种事情，看看有没有什么别的方式，就是正好是不要是两套东西，就是 Git 上一套。然后飞书上一套。只是为了 review， 然后 copy 了一份出来，相当于是。如果能有这种什么映射的方式，然后直接是在 GitHub 上。是说 review 的东西直接是看到的是 GitHub 的东西，但只是只是在飞书里面做，看有没有这种方式。可以看飞书里面有没有这样的功能，我也我也不大清楚。这我我总感觉这种，就是你有多份 copy 的时候，就变的事情就变得很复杂了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:21:40  
其实之前您没有接入的时候，其实它并不是多份 copy， 不过就是它都是在飞书上，只是我两边发而已。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:21:40  
就是，正好只有一份。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:21:51  
但是在飞书上你必一定要发布出去，你要构建这些东西，还是要回到 GitHub 嘛，对吧？你飞书不可能帮你构建了，所以最终你在， GitHub 上必须有一份的这个东西。GitHub 又不能直接从你飞书里面拿东西，所以这个。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:22:06  
对，现在就是他其实遇到一个问题，就是开源，因为开源的文档其实是社区共建嘛，他并不是我们这边生产，所以可能会有用户的就其他的用户的一些提交。对，这个东西我们没有办法恢复，把它弄回飞书，这样的话会很麻烦，就整个，就像你之前，你说今天跟我说你要改 SDK 文档。明天你 SDK， 四个 PR 上来了，我当时都有点慌了。我都不知道该怎么去把你的东西同步过来，后来我整个国庆就一直在同步你这边的东西，所以是的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:22:46  
就现在 SDK 这文档还没有完全的好，就好多东西还缺的，就是你说的那种，什么像有的单独页面，就有些在单独页面的。我看好多都缺。然后链接也不对，所以还得弄。还得弄一。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:23:03  
链接，就是我这边，因为我在整理您的内容的时候，其实我随时发现的问题，我就在那个群里。随时讲了，然后您看到了，你就可以处理一下。没，那然后后面，如果想后面再有什么动作的话，我决定就是还是我们尽快的往刚才说的那条路上走，就是以 web contents 里的内容为主。然后我们在这个上面去建设 Zilliz 的文档，而不是像以前我们是以 Zilliz 为主，然后开源是个副产品，这种思路调换一下。然后我们尽量把这个路线走顺，然后都以 Markdown 为主，然后像验收什么的，到时候我看能不能弄个插件，因为我们现在已经有。就是 Markdown 转飞书的能力和飞书转 Markdown 的能力。就是我们内部的一套脚本，这套脚本到时候像 review 什么的还是可以直接发飞书的，但是 web contents 那就是文档都是以 Markdown 形式交付为主。啊，对。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:24:15  
现在那个 web- content 里面，这些就是 SDK 这些文档的话，主要的骨架都是有的，但是里面的内容，就是里面描述的这些东西。有时候可能不够细啊，或者是比较就是写得比较简单，这种东西，这这种东西它可能 AI 没法帮你干，就是。得不停地加，就是不停地丰富。AI 它也不知道你要想写啥，想写多细它也不知道。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:24:41  
是的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:24:41  
也而且有些东西是写细的话，有可能很快就会过时。这些东西都不当那个。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:24:46  
对，是的，所以我当时就是在做那个 SDK 的信息架构的时候，其实我就考虑过这些问题嘛。我就觉得也不能太细，但是也不能不写，但是当时因为就又又于人力嘛，我这边只有一个人在投入这个事情，要管那么多 SDK。还大概有，算起来有3000多个页面，所以当时是想着说尽量的能够把我这边能呈现的内容呈现出来。但是后，现在有 agent 之后，其实我觉得就像昨天讨论的那个样子，就是能够呈现给用户的信息，在一屏之内能够呈现给用户的信息。就不要分多屏。我大概是这么一个原则，所以就是昨天跟您说的那个其实看上去也不是特别的臃肿啊，就我们正好也讨论一下这个就达成一个共识吧。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:25:42  
就。就是您看，就是像这种，其实这是 describe 的，这是 go 的，就还是这种，其实没有什么缩进嘛。然后 Schema 是分出来的，因为 Schema 我觉得是一个重要的概念，所以它值得分好几篇文档。你昨天问我那个 Java 里面的 collection schema 的下面那些方法，其实您看了，您也可以看一下。就是 collection schema 它是类的页。内页下面，他自己公开的那些公开方法里面，其实也很复杂。比如说我 add fields， 比如说什么 add properties， 这种它其实也很复杂，所以这些页面是值得。做单独的，但是比如说这是枚举类就不说了，枚举都会都会有的，所以枚举也会，也是有单独页面的。这样像 field type， index type。contents consistency level， 这些都是有的。但是有一些页面其实没有必要做，比如说您说的那种就它返回了一个类，这个类下面有什么，很多 getter， 或者是很多 setter。这很多 getter 的这些东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:26:56  
我觉得 getter 是不需要有独立页面的，就直接列在下面，就像我有的页面里写的，就是 parameters 下面会有 methods。那直接就把那些 get 列下来就好了。就是有实际意义。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:27:09  
那个 get set 这个东西。可能，就是不同语言，它可能不太一样，有的语言可能一套 set 有。一套 get 或者一套 set 有好几个方法，有可能有两三个方法，就是他为了那个易用性嘛，有时候会提供就一个成员会提供3个这种 set 或者 get。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:27:33  
这个没关系啊，就是直接列在这个下面了，就是我这里不是 parameters 嘛，然后你下面写 methods， 把 getter 和 setter 都列出来就好了。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:27:34  
然后就嗯反正现在，反正现在总的原则是一些这种基本的类，比如说 collection schema、 field schema 或者什么 function 这些东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:27:43  
因为他的返回，对，他。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:27:52  
单独的页面嘛，是吧？



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:27:53  
对对对。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:27:54  
然后诶枚举还有这种，枚举单独的页面。然后。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:28:01  
你像 CPP 这个我是分层写的，这个 schema 我是展开了的，但是展开其实也不是很乱，也没有太臃肿。啊。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:28:10  
还有一个要遵守的是那个就是 Python 里面，它的 collection schema 这东西是放在之前是放在外外层的。就是 collections 外面。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:28:20  
对，他放在，不是，他放在 ORM 里的，所以。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:28:23  
我现在把它全部挪进去了，就是让它分类挪进去了，就其他语言，因为 Java 是挪进去的，其他语言就是至少要统一，对吧？而且你放在上层，它是不符合分类的这个这上层的分类的概念，所以我全部挪进去了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:28:36  
如果放在上面，诶，不对啊，我之前应该就是放在里面的呀。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:28:40  
没有，之前，我今天早上更新之前是放在外面，现在应该重新 build 过了，现在 Python 的放在里面了。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:28:46  
没有这个。哦，对对， Python 是放在外面的，是的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:28:49  
之前放外面的，我现我现在挪进去了。所以后面这把几条主要的这种规则遵守，就多个源遵守，至少他们股价就是一致的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:00  
嗯嗯嗯，行。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:00  
然后后面再去搞细节。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:03  
可以啊，那就这样，我们并行吧，就是您这边慢慢地调那个 SDK 的 skill， 然后我这边把那个基于开源文档做 Zilliz 文档的这套这条线给它捋平。然后我们后面看能不能在今年年底的时候把这个流程跑通，我觉得应该还是有点挑战的。啊。讲这样的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:28  
反正我这边主要是整这个 Milvus 开源的这部分的东西，然后我后面反正预计的是要把它全部整成自动化的，就是全部。类似于一键自动全部更新完的这种，就是从发布到更新全部完成的这种东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:42  
对的，是的。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:42  
然后那个 res 那边的话，你看郑老师往那走。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:45  
诶，那我想问一下你，就比如说我们这边加了一篇新的 user guide， 您那边怎么知道呢？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:47  
嗯。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:52  
或者我以什么机制通知你？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:54  
加一篇新，飞书上加我是不知道的。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:54  
我不在飞书上。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:29:56  
嗯，飞书上加一篇新的，我没法知道。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:29:59  
你的意思就是说。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:30:00  
因为这飞书上它确实不好弄，飞书上东西你要你要受限于那个飞书的 API 这东西，而且还得让 SQ 去理解这东西。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:30:12  
也就是说，如果如果我们后面改成，就是文档直接在直接在 GitHub 仓库里发的话。您这边就直接扫描到了，是吧？



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:30:22  
对，如果是在 GitHub 仓库里面就好做得多，就是因为这东西 MD 文件嘛，那它很容易就就是过一遍这东西，飞书上面它。你每访问一个文档，就是每去访问一下，它都要调那个飞书 API 的，就是它也慢。一方面慢，不如那个 MD 文件，它直接读磁盘，是快很多。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:30:45  
好，行，我明白了。那就我们就说好，就按这个方向先走走，好吧？然后我这边把整个 CS 文档的架构重新调整一下。那这个可能可能也得花上小半个月或者一个月的时间。



<cite type="user" uid-ref="u3" user-name="Leryn Li"></cite> 00:31:05  
文家，要，我今天中午刚好也在看，要不我这边先梳理一下，到时候下周约个会，找你们两个看一下。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:31:08  
嗯，对。可以可以。



<cite type="user" uid-ref="u3" user-name="Leryn Li"></cite> 00:31:12  
就我把整个流程先梳理一下，然后到时候找你们，你们看一下能不能行得通。然后咱们再一步一步往好看。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:31:20  
好的，可以，没问题。那就这个事情就交给你，好吧？



<cite type="user" uid-ref="u3" user-name="Leryn Li"></cite> 00:31:24  
好，嗯，好。



<cite type="user" uid-ref="u2" user-name="Anthony Tu"></cite> 00:31:24  
好嘞，行，那好，那先谢谢孟老师。嗯。



说话人 1 用 <cite type="user" uid-ref="u1" user-name="Michael Mo"></cite> 的设备 00:31:28  
嗯，行，看一下，嗯嗯。



<cite type="user" uid-ref="u3" user-name="Leryn Li"></cite> 00:31:28  
嗯，谢谢孟老师。嗯。