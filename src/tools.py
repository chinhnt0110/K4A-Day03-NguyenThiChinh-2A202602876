"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "get_fees",
        "description": "Tra cứu báo giá của các dịch vụ pháp lý.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_type": {
                    "type": "string",
                    "description": "Dịch vụ pháp lý"
                },

            },
            "required": ["service_type"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn pháp lý
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - customer_id (string): ID của user
    #    - datetime_str (string): Ngày giờ cần đặt lịch
    #    - lawyer_name (string): Tên luật sư
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn pháp lý",
        "parameters": {
            "type": "object",
            "properties": {
                # TODO 1.2: Khai báo các thuộc tính tham số cho Tool tại đây...
                "customer_id": {
                    "type": "string",
                    "description": "ID của user"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Ngày giờ cần đặt lịch"
                },
                "lawyer_name": {
                    "type": "string",
                    "description": "Tên luật sư"
                }
            },
            "required": ["customer_id", "datetime_str", "lawyer_name"]
        }
    },
    {
        "name": "find_lawyer",
        "description": "Tìm kiếm thông tin luật sư theo tên luật sư, theo mã khách hàng hoặc theo dịch vụ pháp lý.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Mã ID của khách hàng để tra cứu luật sư phụ trách (ví dụ 'KH001')"
                },
                "lawyer_name": {
                    "type": "string",
                    "description": "Họ và tên của luật sư cần tìm kiếm"
                },
                "service_type": {
                    "type": "string",
                    "description": "Dịch vụ pháp lý cần tìm luật sư phụ trách"
                }
            },
            "required": []
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "ly hôn": {
        "lead_lawyer": "Quách Văn Thơm",
        "price": 10000000
    },
    "hành chính": {
        "lead_lawyer": "Bùi Thị Hương",
        "price": 5000000
    },
    "dân sự": {
        "lead_lawyer": "Nguyễn Văn A",
        "price": 5000000
    },
    "thừa kế": {
        "lead_lawyer": "Nguyễn Thị Mai",
        "price": 200000000
    },
    "hình sự": {
        "lead_lawyer": "Trần Quốc Tuấn",
        "price": 10000000
    },
    "đất đai": {
        "lead_lawyer": "Lê Thị Lan",
        "price": 10000000
    }
}

MOCK_CUSTOMER = {
    "KH001": {
        "name": "Nguyễn Thị Chinh",
        "phone": "0989012345",
        "lead_lawyer": "Quách Văn Thơm" 
    },
    "KH002": {
        "name": "Trần Văn Oád",
        "phone": "0912345678",
        "lead_lawyer": "Nơ Long" 
    },
    "KH003": {
        "name": "Lê Thị Cát Bơ",
        "phone": "0934567890",
        "lead_lawyer": "Thỏ" 
    }
}


def execute_get_fees(service_type: str = "", **kwargs) -> str:
    """Thực thi tra cứu báo giá"""
    st = service_type or kwargs.get("service") or ""
    query = str(st).strip().lower()
    service = None
    matched_key = st
    for key, data in MOCK_DATABASE.items():
        if query in key or key in query:
            service = data
            matched_key = key
            break
    if service:
        return json.dumps({
            "status": "SUCCESS",
            "service_type": matched_key,
            "data": service,
            "price": service.get("price", 0),
            "lawyer": service.get("lead_lawyer"),
            "message": f"Phí dịch vụ {matched_key} là {service.get('price', 0):,} VNĐ. Luật sư phụ trách: {service.get('lead_lawyer')}."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dịch vụ '{st}' trong hệ thống bảng giá."
        }, ensure_ascii=False)


def execute_schedule_appointment(customer_id: str = "KH001", datetime_str: str = "09:00 ngày mai", lawyer_name: str = "Quách Văn Thơm", **kwargs) -> str:
    """Thực thi đặt lịch hẹn tư vấn pháp lý"""
    cid = customer_id or kwargs.get("student_id") or "KH001"
    dt = datetime_str or kwargs.get("time") or "09:00 ngày mai"
    lawyer = lawyer_name or kwargs.get("advisor_name") or "Quách Văn Thơm"
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{cid}-99",
        "customer_id": cid,
        "datetime": dt,
        "lawyer": lawyer,
        "message": f"Đặt lịch thành công cho khách hàng {cid} với luật sư {lawyer} vào lúc {dt}."
    }, ensure_ascii=False)


def execute_find_lawyer(service_type: str = None, customer_id: str = None, lawyer_name: str = None, **kwargs) -> str:
    """Thực thi tìm kiếm luật sư phụ trách theo mã khách hàng, tên luật sư hoặc dịch vụ pháp lý"""
    cid = customer_id or kwargs.get("customer_id")
    st = service_type or kwargs.get("service_type")
    lname = lawyer_name or kwargs.get("lawyer_name") or kwargs.get("name")

    # 1. Tra cứu theo mã khách hàng
    if cid:
        c_id = str(cid).strip()
        if c_id in MOCK_CUSTOMER:
            lawyer = MOCK_CUSTOMER[c_id].get("lead_lawyer", "Chưa phân công")
            cust_name = MOCK_CUSTOMER[c_id].get("name", "")
            return json.dumps({
                "status": "SUCCESS",
                "customer_id": c_id,
                "customer_name": cust_name,
                "lawyer": lawyer,
                "message": f"Tìm thấy luật sư phụ trách cho khách hàng {c_id} ({cust_name}): {lawyer}"
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "NOT_FOUND",
                "message": f"Không tìm thấy thông tin khách hàng với mã {c_id} trong hệ thống."
            }, ensure_ascii=False)

    # 2. Tra cứu theo tên luật sư
    if lname:
        query = str(lname).strip().lower()
        found_lawyers = []
        for key, data in MOCK_DATABASE.items():
            lawyer = data.get("lead_lawyer", "")
            if query in lawyer.lower() or lawyer.lower() in query:
                found_lawyers.append((lawyer, f"dịch vụ {key}"))
        for cust_id, cdata in MOCK_CUSTOMER.items():
            lawyer = cdata.get("lead_lawyer", "")
            if query in lawyer.lower() or lawyer.lower() in query:
                found_lawyers.append((lawyer, f"khách hàng {cust_id}"))

        if found_lawyers:
            lawyer_found, domain = found_lawyers[0]
            return json.dumps({
                "status": "SUCCESS",
                "lawyer": lawyer_found,
                "message": f"Tìm thấy luật sư {lawyer_found} phụ trách {domain} trong hệ thống."
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "NOT_FOUND",
                "message": f"Không tìm thấy luật sư nào có tên '{lname}' trong hệ thống của văn phòng."
            }, ensure_ascii=False)

    # 3. Tra cứu theo dịch vụ pháp lý
    if st:
        query = str(st).strip().lower()
        matched_service = None
        matched_data = None
        for key, data in MOCK_DATABASE.items():
            if key in query or query in key:
                matched_service = key
                matched_data = data
                break

        if matched_data:
            lawyer = matched_data.get("lead_lawyer", "Chưa phân công")
            return json.dumps({
                "status": "SUCCESS",
                "service_type": matched_service,
                "lawyer": lawyer,
                "message": f"Tìm thấy luật sư phụ trách cho dịch vụ {matched_service}: {lawyer}"
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "NOT_FOUND",
                "message": f"Không tìm thấy luật sư phụ trách cho dịch vụ '{st}' trong hệ thống."
            }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": "Không tìm thấy thông tin yêu cầu. Vui lòng cung cấp mã khách hàng, tên luật sư hoặc loại dịch vụ pháp lý."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "get_fees": execute_get_fees,
    "schedule_appointment": execute_schedule_appointment,
    "find_lawyer": execute_find_lawyer,
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
