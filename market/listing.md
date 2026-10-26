# 推广素材：会议成本

> 这个会一年烧掉多少钱，能砍掉多少。

下面每条文案都用本仓脚本测过 AI 味。

---

## 一、GitHub 仓库元信息

**About**：见仓库设置（已由发布脚本写入）。

**Social preview**：`market/social-preview.png`（1280×640，已生成）。


---

## 二、小红书

**标题（5 选 1）**

1. 算了一下我们周会的钱，我沉默了
2. 一个 11 人的周会，一年 9.9 万
3. 老板说这个会很重要，我算了个数给他看
4. 每天 30 分钟的站会，其实是最贵的会
5. 「开会不花钱」是我听过最大的错觉

**正文**

我把我们周会的成本算了一遍，然后拿着数字去找老板了。

**11 个人，每周 1 小时，一年 9.9 万。**

怎么算的：时薪 = 月薪 ÷ 21.75 ÷ 8。人均 2.2 万的话，时薪约 126 元。

但很多人漏了两个东西：

1️⃣ **会前准备和会后恢复**。一个「1 小时的会」，实际占用约 85 分钟/人。加上这一项，成本立刻涨 42%。

2️⃣ **企业综合成本**。社保公积金、工位、设备，通常再加 30–50%。按 1.4 倍算，这个会一年是 13.8 万。

换算成能感知的东西更狠：**一年消耗 97 个工作日**——一个 11 人的团队，每年有四个多月的人力坐在同一间会议室里。

最反直觉的一个发现：

**看起来最便宜的站会，其实是最贵的。**

6 个人、每天 30 分钟，单次只要 695 元。但一年开 250 次，总共 17.4 万——比 11 人周会还贵。

因为贵不贵看频率，不看单次。

我给老板的方案不是「取消」，是：

11 人 60 分钟周会 → 7 人 20 分钟双周会
年成本 9.9 万 → 1.66 万，省 83%

会前发一页纸材料，会上只讨论有分歧的两三条，单周的进度用文档异步同步。

他同意了。

零依赖，一个 py 文件。所有数字都能用 --json 复现。

`#职场` `#会议` `#效率` `#打工人` / `#向上管理` `#时间管理` `#职场干货` / `#我的工作日常`

**首评（置顶）**

说句实话：一对一（2 人 30 分钟每周）一年只要 1.16 万，是这张表里 ROI 最高的一类。别把「砍会议」砍成「不沟通」。


---

## 三、X / Twitter（英文）

```
Someone said "it's just one hour a week." So I did the math.

11 people × 85 min (meeting + prep + context-switch) × ¥126/hr × 50 weeks
= ¥98,515/year ≈ 97 person-days.

That's a 11-person team spending four-plus months of headcount sitting in one room.

The counterintuitive result: the cheapest-looking meeting is the most expensive.

6-person daily standup: ¥695 per meeting. But 250 times a year = ¥173,851 —
more than the weekly. Frequency dominates unit cost.

Shipped a calculator. Zero deps, every number reproducible with --json.
```


---

## 四、Show HN

```
Show HN: Meeting-cost – turn a recurring meeting into a number

The argument "this meeting is unnecessary" never wins. "This meeting costs
98,515 a year and we could get it to 16,595" does.

Model:
  hourly = monthly_salary / 21.75 / 8
  per_meeting = people × (duration + 15 prep + 10 recovery) / 60 × hourly
  annual = per_meeting × frequency

Two things people under-count, both included by default: prep and
context-switch time (~85 min occupied for a "1 hour" meeting), and employer
overhead (`--loaded 1.4` for social insurance, desk, equipment).

The result that surprised me: the daily 30-minute standup is the most expensive
item on the list. ¥695 per instance looks trivial until you multiply by 250.

Output also includes a minimization path (fewer people / shorter / lower
frequency) with the resulting savings, because "cancel it" is rarely actionable
and "7 people, 20 minutes, biweekly" is.

Caveats: it's an estimate, not accounting. It can't price the cost of
interrupting someone's afternoon, which is often larger than the meeting.

github.com/zhbehx/meeting-cost
```


---

## 五、发布清单

| 渠道 | 素材 | 关键动作 |
| --- | --- | --- |
| GitHub | Release v1.0.0 | 已发布 |
| X | 上面的英文稿 | 配终端截图，分数可见 |
| Show HN | 上面的 HN 稿 | 周二至周四 UTC 14:00–16:00 |
| 社群 / 即刻 | 一句话 + 链接 | 只讲一个点，别贴 README |