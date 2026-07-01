let ws;

function send() {

    // 清空
    ["glm","qwen","kimi","deepseek"].forEach(id=>{
        document.getElementById(id).innerHTML = "";
    });

    ws = new WebSocket("ws://127.0.0.1:8000/ws/compare");

    ws.onopen = () => {
        ws.send(JSON.stringify({
            message: document.getElementById("input").value
        }));
    };

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);

        const box = document.getElementById(data.model);

        if (box) {
            box.innerText = data.data;
        }
    };

    ws.onclose = () => {
        console.log("连接关闭");
    };
}