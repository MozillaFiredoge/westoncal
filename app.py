from flask import Flask, request, render_template, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calculate_errors(data, mode):
    """通用计算函数"""
    
    # 误差计算模式
    if mode == 'error':
        R1 = float(data['R1'])
        R2 = float(data['R2'])
        R0 = float(data['R0'])
    
        k = R1 / R2
        Rx = k * R0
        delta_R1 = float(data['delta_R1'])
        delta_R2 = float(data['delta_R2'])
        delta_R0 = float(data['delta_R0'])  # 电阻箱精度误差
        
        term1 = (k * delta_R1 * R0 / R1) ** 2
        term2 = (k * delta_R2 * R0 / R2) ** 2
        term3 = (k * delta_R0) ** 2
        error_resistor = math.sqrt(term1 + term2 + term3)
        
        sensitivity = float(data['sensitivity'])
        error_sensitivity = Rx * 0.2 / sensitivity
        
        total_error = math.sqrt(error_resistor**2 + error_sensitivity**2)
        
        return {
            "k": k,
            "Rx": Rx,
            "error_resistor": error_resistor,
            "error_sensitivity": error_sensitivity,
            "total_error": total_error
        }
    
    # 灵敏度计算模式
    elif mode == 'sensitivity':
        R0_sens = float(data['R0_sens'])  # 电阻箱的标称值
        delta_R0_change = float(data['delta_R0_change'])  # 电阻变化量
        delta_n = float(data['delta_n'])                  # 偏转格数
        
        relative_change = delta_R0_change / R0_sens
        sensitivity = delta_n / relative_change if relative_change != 0 else 0
        
        return {
            "sensitivity": sensitivity,
            "relative_change": relative_change
        }

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        if data['mode'] == 'error':
            result = calculate_errors(data, 'error')
            return jsonify(result)
        elif data['mode'] == 'sensitivity':
            result = calculate_errors(data, 'sensitivity')
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)