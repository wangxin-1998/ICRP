# ICRP正式开发版

## 分支说明
**master分支**，即主分支。任何项目都必须有个这个分支。对项目进行tag或发布版本等操作，都必须在该分支上进行。  

**develop分支**，即开发分支，从master分支上检出。团队成员一般不会直接更改该分支，而是分别从该分支检出自己的feature分支，开发完成后将feature分支上的改动merge回develop分支。同时release分支由此分支检出。 

**feature分支**，即功能分支，从develop分支上检出。团队成员中每个人都维护一个自己的feature分支，并进行开发工作，开发完成后将此分支merge回develop分支。此分支一般用来开发新功能或进行项目维护等。

[参考网址1](https://www.cnblogs.com/yhaing/p/8473746.html)

[参考网址2](https://www.cnblogs.com/pbrong/p/Arong.html)

---
## 分支的创建与合并

[GitHub分支创建及合并参考教程](https://blog.csdn.net/qq_30607843/article/details/84404000)
