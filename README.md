# Graph Search Algorithm Visualizer with Tkinter

Chương trình mô phỏng đồ thị trực quan bằng Python và Tkinter. Mỗi node được vẽ như một ngôi nhà kèm mặt trời hiển thị trọng số. Mỗi edge là đường thẳng nối hai node, có biển báo chi phí với cây chống thẳng đứng. Node ID và Edge ID là duy nhất, thuận tiện cho truy xuất và chỉnh sửa.

Cấu trúc dữ liệu:

- `nodes`: lưu trữ tất cả node với ID duy nhất. Mỗi node chứa tọa độ `(x, y)`, bán kính `r`, trọng số hiển thị và các đối tượng canvas (vòng tròn, mái nhà, mặt trời, chữ ID).
- `edges`: lưu trữ tất cả edge với ID duy nhất. Mỗi edge nối hai node (`n1`, `n2`), có chi phí (`cost`), đối tượng canvas của đường nối (`item`), biển báo (`sign`) và cây chống (`pole`). Chi phí hiển thị trực tiếp trên biển báo.

Chương trình tạo sẵn 5 node và 6 edge mẫu, có thể thêm node mới bằng `create_node(x, y, weight)` và thêm edge mới bằng `create_edge(n1_id, n2_id, cost)`. Biển báo luôn nằm ngang, cây chống luôn thẳng đứng, chi phí và trọng số hiển thị trực tiếp trên canvas.
