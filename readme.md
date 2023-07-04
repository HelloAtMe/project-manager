## 实现功能

1. 针对 python + pyside6 环境开发的项目
2. 实现 项目创建 项目编译 项目打包 三个功能
3. 编译用工具 nuitka， 打包用工具 Inno Setup
4. 本项目用 tkinter 开发

## 使用

### 新建项目

1. 运行 new.pyw
2. 填写 项目名称  和 项目描述
3. 确定按钮 生成新项目
4. 在使用前注意，需要在代码中 设置 仓库的位置:  `9 RepositoryPath = r'D:\Yun\Codes\Python'`

### 编译打包项目
1. 设置 ISCC_Compiler
2. 设置 proj_desc_file = r'D:\Yun\Codes\Python\hellp\hellp.pyui-proj'
3. 设置 version = 'beta1.0.0'
4. 运行 compile.pyw

