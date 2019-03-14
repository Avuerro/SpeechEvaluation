# Speech Enhancement Tools（SETools）

- [x] 计算语音增强相关的评价指标，计算结果会被保存为 Excel 表格。
- [] 自动下载 TIMIT 与 NoiseX92，并合成噪声

## Usage

安装 

```shell
# 手动安装 PESQ Wrapper @vBaiCai
git clone https://github.com/vBaiCai/python-pesq.git
cd python-pesq
python setup.py install

pip intall SETools
```

使用方法：

```shell
Speech Enhancement Tools

optional arguments:
  -h, --help            
                        show this help message and exit
  --nosiy_dir NOSIY_DIR
                        带噪语音目录
  --denosiy_dir DENOSIY_DIR
                        降噪语音的目录
  --clean_dir CLEAN_DIR
                        纯净语音的目录
  --output_path OUTPUT_PATH
                        评价指标存储的全路径，必须以拓展名 .xls 结尾
  --limit LIMIT         
                        被测试语音的数量。默认为0，表示不限制数量
  --offset OFFSET       
                        从某个索引位置开始计算评价指标，默认为0，表示从索引为 0 的语音开始计算
  --sr SR               
                        语音文件的采样率
```

例如：

```shell
SETools --nosiy_dir /media/imucs/DataDisk/haoxiang/Release/speech_enhancement/release_-5_0_30_50/test/noisy/ --denosiy_dir ../se_-5_0_30_50_VCC/output/ --clean_dir /media/imucs/DataDisk/haoxiang/Release/speech_enhancement/release_-5_0_30_50/test/clean
```
