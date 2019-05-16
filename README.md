# Generic-Subprograms-Implementation
# 程式語言課程實作 generic subprograms

[TOC]

# 一、做法

## 1.   題目定義

### 1.1 簡介

實作 Generic Sorting 以及 Generic Searching，以滿足各 Data type 通用的排序及搜尋功能（Generic 實作策略請見4. 特別說明 c. Generic 實作策略），並且不可使用語言內建的 sort, search functions。
在此實作了五種 Sorting (分析請見3. 演算法 a. 排序)，以及兩種 Searching (分析請見3. 演算法 b. 搜尋)。
並且可接受以檔案輸入或以鍵盤輸入（詳細定義請見 b. 使用者可用功能 & c. 資料輸入／輸出詳細說明）。
以視窗介面作為呈現與操作入口（請見執行結果）。

### 1.2 使用者可用功能（簡列） 

- 輸入
  - 檔案路徑
  - 直接輸入資料
- 執行功能
  - Sorting
  - Searching
- Sorting 方式
  - 排序方法
    - Bubble Sort
    - Selection Sort
    - Insertion Sort
    - Merge Sort
    - Quick Sort
  - 排序順序
    - ASCII 小到大
    - ASCII 大到小
    - 拼音 小到大 （因應中文而設）
    - 拼音 大到小 （因應中文而設）
- Searching 方式
  - Linear Search
    - 部分匹配搜尋
    - 全部匹配搜尋
  - Binary Search （資料需先以 ASCII 小到大排序過）
    - 全部匹配搜尋

### 1.3 資料輸入／輸出詳細說明

- 輸入
  - 路徑
    - txt 檔
      檔案內容將被分割（以逗號（全型／半型）、分號（全型／半型）、換行）。
    - json 檔
      遵循 json 檔案形成標準。
  - 直接輸入
    - 數字／文字
      資料將將被分割（以逗號（全型／半型）、分號（全型／半型）、換行）。
    - List
      第一個字元須為"["，最後一個字元須為"]"。之間的字元將由半型逗號所切割成元素。
    - Dictionary
      如同 json 檔形成的字典標準。
  - 搜尋的內容
    - json 檔／Dictionary
      只能搜尋 key。
    - 其他
      輸入搜尋內容。
- 輸出
  - Sorting
    - json 檔／Dictionary
      以 key 作為排序依據，輸出將以Dictionary呈現。
    - 其他
      分割後的元素作為排序依據，輸出將其元素換行呈現。
  - Searching
    - json 檔／Dictionary
      將輸出符合其搜尋結果的{key: value}。
    - 其他
      將輸出符合其搜尋結果的是哪幾個分割後的元素（第幾個）。

## 2.  資料結構

### 2.1 class Processor

####
類似工廠的角色，統一以此類別的實例進行操做。

#### 成員變數結構

- origianl_input
  - type: string
  - 原本 input 的 string
- original_type
  - type: type
  - type or original_input
- modules_list
  - type: list
  - 元素構成是已經 import 的 module名稱 (string)(module裡面是會用來實際操作排序或搜尋的實例的class)。
- actual_instance
  - type: 看實際情況。
  - 實際操作排序或搜尋的實例
- actual_type
  - type: type
  - type of actual_instance
- is_path
  - type: boolean
  - input 是否為路徑

### 2.2 class Sorting

#### 
定義 Sorting 的介面（由於python 無 interface，這裡實作策略請見4. 特別說明 c. Generic 實作策略）。

#### 成員變數結構

無

### 2.3 class Searching

#### 
Searching 的介面（由於python 無 interface，這裡實作策略請見4. 特別說明 c. Generic 實作策略）。

#### 成員變數結構

無

### 2.4 class DataType

#### 
設計來當所有實際操作排序、搜尋的實例的父類別。

#### 成員變數結構

- sign
  - type: string
  - 用來標誌 type，主要為了方便以檔案副檔名去對照要使用哪一種 class type。

### 2.5 class List

#### 
包裝內建 list 物件，並實作 Sorting 和 Searching 的類別。

#### 成員變數結構

- inner_list
  - type: list
  - 內建型的 list，最底層真正的操作實例。

### 2.6 class Dictionary

#### 
包裝內建 dict 物件，並實作 Sorting 和 Searching 的類別。

#### 成員變數結構

- inner_dict
  - type: dict
  - 內建型的 dict，最底層真正的操作實例。

### 2.7 class File

#### 
需要經過檔案讀取的物件的父類別。

#### 成員變數結構

- path
  - type: string
  - 檔案路徑。

### 2.8 class FileText

#### 
包裝讀取 txt 檔案後的物件，並實作 Sorting 和 Searching 的類別。

#### 成員變數結構

- data_list
  - type: list
  - 讀取完文字檔案後，並將其文字分割後的 list。
- prepare_list
  - type: List
  - 將 data_list 包裝成 List，方便統一進行操作。

### 2.9 class FileJson

#### 
包裝讀取 json 檔案後的物件，並實作 Sorting 和 Searching 的類別。

#### 成員變數結構

- data_dict
  - type: dict
  - 讀取完 json 檔案後的 dict。
- prepare_dict
  - type: Dictionary
  - 將 data_dict 包裝成 Dictionary，方便統一進行操作。

## 3.   演算法

### 3.1 排序

#### 3.1.1 Bubble Sort

##### 作法

重複地訪問要排序的陣列，一次比較相鄰兩個元素，如果兩個之間的順序錯誤（看要小到大還是大到小）就交換兩者，一次訪問後會固定下最後一個確認大小的元素。
如此一直重複直到不需要交換（排序完成）。

##### 時間複雜度

不優化的情況下，假如陣列長度為ｎ，所有人都需要走訪。
	且需重複走訪，只是每次可以少一個，也就是 ｎ－１。
	所以平均／最壞時間複雜度為 O(n2)。
	最佳情況為一次走過，都不需要交換，便為 O(n)。

##### 空間複雜度

需要一個空間進行交換，所以空間複雜度為 O(1)。

#### 3.1.2 Selection Sort

##### 作法

從剩餘還沒排序的陣列中找最小（大）元素，然後放到已經排序好的陣列的最後一個位置。重複以上動作直到排序完成。

##### 時間複雜度

不優化的情況下，假如陣列長度為 ｎ。
最佳／平均／最差的時間複雜度都是 O(n2)。

##### 空間複雜度（輔助）

需要一個空間進行交換，所以空間複雜度為 O(1)。
但比起氣泡排序的交換情況，這個最佳可以到都沒有交換的情況，所以效能上還是比氣泡排序佳。

#### 3.1.3 Insertion Sort

##### 作法

從還沒排的陣列中取出一元素，由後往前和已經排好的陣列比較，直到遇到不大於自己的元素後插入此元素，如果都找不到則插入在最前面。重複以上動作直到排序完成。

##### 時間複雜度

不優化的情況下，假如陣列長度為 ｎ。
最差／平均為都是 O(n2)。
最佳情況為 O(n)。

##### 空間複雜度（輔助）

需要一個空間進行交換，所以空間複雜度為 O(1)。

#### 3.1.4 Merge Sort

##### 作法

不斷把陣列分成兩邊（Divide & Conquer 的策略，可以有遞歸或迭代作法），等到剩下一個元素的時候，再開始依據元素大小將兩邊的陣列合併。 
在此以遞歸作法實作。

##### 時間複雜度

不優化的情況下，假如陣列長度為 ｎ。
單次中需要走過所有元素且放入新的子陣列中，所以為 O(n)。
遞歸幾次便是要除幾次 2，也就是 O(log2n)
所以總共最壞與平均是 O(n*log2n)。
而最佳情況為O(n)。

##### 空間複雜度（輔助）

因為每次要開新空間來存放成新的陣列，所以為 O(n)。

#### 3.1.5 Quick Sort

##### 作法

與 Merge Sort 一樣採用 Divide & Conquer 的策略（在此依舊採用遞歸實作。）。
不過在切割的部分與 Merge Sort 不同的是，Merge Sort 每次 Divide 都是直接拆半（原始作法的話），而 Quick Sort 每次怎麼切是和當次選到的基準點有關。
每次挑選基準點，掃描當前處理陣列，把比基準點小的值放入左邊的陣列，大的放到右邊，最後再把左右兩邊的陣列重複以上動作，最後將排序後的陣列回傳。 

##### 時間複雜度

```
不優化的情況下，假如陣列長度為 ｎ。
```

最佳／平均為 O(n*log2n)。
但最壞為 O(n2)，也就是每次取基準點時都剛好取到最大／最小的，但是因為這種機率不高，所以普遍而言這種排序法還是被認為最快的。

##### 空間複雜度（輔助）

因為每次要開新空間來存放成新的陣列，所以為 O(n)。

### 3.2 搜尋

#### 3.2.1 Linear Search

##### 作法

依序走訪過陣列裡全部元素，直到找到或者到最後。
但本實作中，則是做了兩種，一個是完全匹配設定為找到便結束，但是部分匹配的是無論有無找到適合的，依舊會確認完所有元素。

##### 時間複雜度

不優化的情況下，假如陣列長度為 ｎ。
平均與最差為全部走訪過，也就是 O(n)。
最好的情況為第一個就找到，也就是 O(1)。

#### 3.2.2 Binary Search

##### 作法

因為需要比大小，所以輸入的陣列需要先排列過。
從陣列的中間元素開始找，如果要找的元素大於或者小於中間元素，則在陣列大於或小於中間元素的那一半中尋找（一樣從中間元素開始比）。

##### 時間複雜度

不優化的情況下，假如陣列長度為 ｎ。
因為每次砍半查找，所以最差／平均情況為 O(log2n)。
但若剛好第一個比對便找到，也就是最佳情況 O(1)。

## 4.  特別說明

### 4.1 源碼語言

Python3

### 4.2 使用函式庫

- sys
- io
- os
- time
- re
- copy
- json
- codecs
- tkinter
- collections
- abc
- inspect
- pypinyin => 參考 https://github.com/mozillazg/python-pinyin

### 4.3 Generic 實作策略

由於 Python 沒有像 Java 一樣的 interface 的定義，這裡是借用了 abc module 裡的 ABCMeta metaclass 還有 abstractmethod 的裝飾來模擬像是 interface 一樣的定義，也就是 class Sorting & class Searching 這兩個 class 其實在定位上是 interface，其他型態需要來實作他們以達到泛型。
另外定義了一個 class Processor 這個像是工廠的角色，所有輸入的資料都會被它包起來，在裡面有一套辨識方法會決定實際上操作的實例該是哪一種型態，所以對外部來說，儘管把資料以它來包裝，不用管實際型態問題。
而此識別方法是所有有實作 Sorting 和 Searching 的 類別，都共同有一個 class 層級的 method，還有一成員變數為"sign"，Processor 會借用 inspect module 去掃描這些 class 的 sign，找到適合的類別。

### 4.4 程式特別處理功能

- 中文字依拼音進行比大小（借助外部庫"pinyin"的幫忙，請見程式碼 utils.py的 pinyin_str、to_pinyin_dict函式）。
- 有一個專門處理最後要顯示出來的字串該怎麼串接的函式（ utils.py 的 to_string）。

# 二、程式碼（略）

# 三、執行結果（略）

# 四、討論

## 1. 動態型態語言？無型態語言？泛型？

- 困難點：一時想不清，如果原本就是動態語言或是無型態的語言，要怎麼做泛型。
- 結果：其實僅僅是被那一句「能處理任意 data types 的資料排序與搜尋」給唬住了，一時卡在「本來就可以自由變動型態，要怎麼做泛型。」後來才釐清了下泛型的意義，還有 Python 型態的意義。但可能這裡實作的不是很好，但已經盡量達到類似配出去根據型態再去綁定實作的函數，只是目前看來有點過度包裝，應可以更精簡。

# 五、心得

## 1. 未完成的遺憾

原先在輸入的檔案格式中，想一併處理 xls, xlsx, csv 等資料處理中經常碰到的檔案，所以在 data_type.py 中也定義好了其要包裝的 class，但最終並還未完成。

## 2. 明顯缺失

## 2.1 字典型態／拼音排序的演算法劣化

在演算法的部分討論了各個排序與搜尋的複雜度，但仔細看個人實作的方法便會發現，在處理字典的部分和特別添加上去以拼音作為排序依據的部分，會劣化掉原先的時間以及空間的複雜度。因為實作的方法會多一次走訪複製元素，最後排完又會再對照複製下來的元素重新並成一個字典。未來應該想辦法優化這些多出來步驟。

## 2.2 泛型處理

在這裡處理泛型的手法其實是理想上的，因為實際操作上可能會有很大機率的人工缺失。因為這裡的介面與實作都是模擬的程序，不像 Java 一樣會有提示作用（若忘了實作）。並且有一層層複雜的繼承、實作、重寫函數，所以後續擴充上如果在一個細節上沒注意到就可能達不成。未來應修正這些做法，例
