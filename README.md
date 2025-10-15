# README NHÓM 07
**Nhóm thực hiện:** 07

**Thành viên:** Nguyễn Sư Thành Đạt
**Mã số sinh viên:** 23110131
**Thành viên:** Trịnh Đại Nghĩa
**Mã số sinh viên:** 23110131
**Thành viên:** Trần Huỳnh Chí Nguyên
**Mã số sinh viên:** 23110131


**Môn học/lớp:** Trí tuệ Nhân tạo/ARIN330585_05CLC

**Ngày nộp:** 15/10/2025

---
## Graph Search Algorithm Visualizer


### Tổng Quan

Chương trình mô phỏng đồ thị trực quan bằng Python, thể hiện bằng GUI với sự hỗ trợ của CustomTkinter, tkinter. Mỗi node được vẽ như một ngôi nhà kèm mặt trời hiển thị trọng số. Mỗi edge là đường thẳng nối hai node, có biển báo chi phí với cây chống thẳng đứng. Node ID và Edge ID là duy nhất, thuận tiện cho truy xuất và chỉnh sửa.

---

### 1. Mục đích xây dựng

Project hướng đến mô phỏng cách các thuật toán tìm kiếm tìm đường đi trên đồ thị. Với Start_node và Goal_Node, thuật toán sẽ dựa trên điểm start và cố gắng tìm đến goal theo logic của thuật toán đó, qua đó ta có thể nhìn nhận, đánh giá từng thuật toán thông qua thời gian và số bước để đi đến goal_node của thuật toán đó.

Project được xây dựng nhằm vận dụng, học hỏi thêm về kiến thức **Trí tuệ Nhân tạo**. Nhóm đã triển khai nhóm thuật toán: 
  - `Uninformed Search`: Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deeping Search (IDS)
  - `Informed Search`: Greedy Best-First Search, A* Search, Uniform Cost Search (UCS)
  - `Local Search`: Hill Climbing, Simulated Annealing, Genetic
  - `Complex Enviroment`: AND-OR Search, Belief State Search, Partially Observable Search
  - `Constraint Satisfaction Problem Search`: Backtracking, Forward-Checking, AC-3

---

### 2. Tính năng chính
Giao diện mô phỏng trực quan (Main Window): gồm 3 phần
  - Phần bên trái: Nơi chứa các nhóm thuật toán. Dùng để chọn 1 thuật toán bất kỳ.
  - Phần giữa: Thuật toán được chọn sẽ hiển thị ở bên trên. Có 2 phần nhỏ gồm:
    - Phần input: có textbox Start_node và textbot Goal_node dùng để người dùng xác định vị trí bắt đầu và kết thúc trên đồ thị. Có 1 nút Random Cost dùng để random lại Cost trên đồ thị ở phần Mini Map.
    - Phần Mini Map: Một mini map của đồ thị sẽ được show ra ở bên dưới phần input, đó sẽ là đồ thị mà thuật toán dùng để mô phỏng đường đi bắt đầu từ `Start_node` và kết thúc ở `Goal_node`. Có 2 nút ở phần Mini Map:
      - Nút `Run Algorithm`: Bắt đầu chạy thuật toán. Nút `Run Algorithm` sẽ gọi sự kiện và 1 window phụ `RunCodeWindow` sẽ xuất hiện để chạy thuật toán.
      - Nút `View Code`: Một window phụ `ViewCodeWindow` sẽ xuất hiện để cho xem cách nhóm xây dựng thuật toán đang được chọn.
  - Phần bên phải: là 1 Log History, dùng để lưu lại tất cả kết quả tìm thấy được sau mỗi lần chạy 1 thuật toán. Log History sẽ luôn lưu và không mất cho đến khi chương trình được tắt. Có 1 nút `Close App` ở bên dưới Log History

Giao diện RunCodeWindow (Window phụ dùng để chạy thuật toán): có 2 phần
  - Phần đồ thị: dùng để người dùng quan sát cách thuật toán chạy trên thuật toán. Nút `Close` dùng để tắt Window RunCode và quay lại Main Window.
  - Phần log & trạng thái: ghi lại từng bước duyệt và di chuyển của thuật toán. Có thông báo kết quả. Có 2 nút `Bước Trước ` và ` Bước Kế ` giúp người dùng quan sát lại theo từng bước di chuyển. Tránh gây sự khó hiểu khi sử dụng chương trình.

Giao diện ViewCodeWindow (Window phụ dùng để xem các hàm thuật toán): Hàm thuật toán được chọn và các hàm phụ, hàm con sẽ được in ra dưới dạng `readonly`. Có nút `Close` để quay lại Main Window.

---

### 3. Yêu cầu.
- Ngôn ngữ lập trình: `Python`
- Trình sử dụng và quản lý Project: Visual Studio.
- Các thư viện được xài: `customtkinter`, `tkinter`, `math`, `random`.
- Thư viện cần cài đặt: Customtkinter
    Cài trong Command hoặc PowerShell: `pip install customtkinter`

---

### 4. Cách sử dụng

- Chạy ứng dụng có tên file: `23110131_TrinhDaiNghia_BaitapCanhan.py`
- Chọn thuật toán: có tất cả 5 combobox cho 5 nhóm thuật toán.
  - Chọn 1 thuật toán trong 5 nhóm thuật toán.
  - Khi chọn xong, các combobox còn lại sẽ tự động khóa
- Chạy thuật toán:
  - Chọn Start_node và Goal_Node. Có thể tùy ý nhấn `Random Cost` để đây đổi Cost. 
  - Nhấn nút `Run` để bắt đầu chạy thuật toán.
  - Quan sát thuật toán chạy trên đồ thị. Đồng thời phần `Log & Trạng thái ` sẽ luôn cập nhật cho mỗi bước đi thành công.
- Để chạy lại thuật toán: Có thể nhấn nút ` Bước Trước ` tới khi nào phần hiển thị ` Bước 0/... `. Hoặc ta sẽ tắt window đó và chọn `Run` lại.
    -  Có thể chọn một thuật toán khác để chạy, có thể random cost mới nhưng Log-History sẽ luôn ghi nhận.
- Có thể xem qua đoạn code thuật toán đang chọn thông qua View Code.

---

### 5. Cấu trúc Code

- File Nhom07_Project_AI.py chính để chạy chương trình
- 1 Module, trong đó gồm:
    - CenterWindow.py: file căn giữa Window
    - GraphData.py: file dữ liệu đồ thị
    - GraphVisualizer.py: file tạo đồ thị
    - UIComponents.py: file UI chính của chương trình
    - UninformedSearch.py: file chứa các hàm thuật toán: Breadth-First Search (BFS), Depth-First Search (DFS), Iterative Deeping Search (IDS)
    - InformedSearch.py: file chứa các hàm thuật toán: Greedy Best-First Search, A* Search, Uniform Cost Search (UCS)
    - LocalSearch.py: file chứa các hàm thuật toán: Hill Climbing, Simulated Annealing, Genetic
    - ComplexEnviroment.py: file chứa các hàm thuật toán: AND-OR Search, Belief State Search, Partially Observable Search
    - CSP.py: file chứa các hàm thuật toán: Backtracking, Forward-Checking, AC-3
    - RunCodeWindow.py: file chạy thuật toán
    - ViewCodeWindow.py: file view hàm thuật toán
      
---

### 6. Những gì đã làm được

- Cấu hình, cài đặt UI. Một số thuật toán:
  - UninformedSearch.py: Depth-First Search (DFS)
    - InformedSearch.py: file chứa các hàm thuật toán: A* Search
    - LocalSearch.py: file chứa các hàm thuật toán: Hill Climbing
    - ComplexEnviroment.py: file chứa các hàm thuật toán: Belief State Search
    - CSP.py: file chứa các hàm thuật toán: Forward-Checking


