"""
Plantilla de ejecución para JavaScript (Node.js)
Combina el código del usuario con los tests ocultos
"""

// CÓDIGO DEL USUARIO
{user_code}

// FUNCIÓN PRINCIPAL DE TESTING
function __runTests() {
    const tests = {tests_json};
    const results = [];
    let totalTime = 0;
    
    for (let i = 0; i < tests.length; i++) {
        const test = tests[i];
        const testInput = test.input || '';
        const expectedOutput = test.expected || '';
        const testName = test.name || `Test ${i + 1}`;
        
        try {
            // Medir tiempo
            const startTime = process.hrtime.bigint();
            
            let actualOutput = '';
            
            if (test.function_call) {
                // Si el test especifica una función a llamar
                const funcName = test.function_call.name;
                const funcArgs = test.function_call.args || [];
                
                // Llamar a la función del usuario
                const result = global[funcName](...funcArgs);
                actualOutput = String(result).trim();
                
            } else if (test.code) {
                // Si hay código específico para ejecutar
                actualOutput = String(eval(test.code)).trim();
            } else {
                // Ejecutar con input simulado
                actualOutput = expectedOutput; // Placeholder
            }
            
            const endTime = process.hrtime.bigint();
            const elapsedTime = Number(endTime - startTime) / 1_000_000_000;
            totalTime += elapsedTime;
            
            // Comparar salidas
            const expectedClean = String(expectedOutput).trim();
            const passed = actualOutput === expectedClean;
            
            results.push({
                name: testName,
                passed: passed,
                time: elapsedTime,
                expected: expectedClean,
                actual: actualOutput
            });
            
        } catch (error) {
            const endTime = process.hrtime.bigint();
            const elapsedTime = Number(endTime - (startTime || 0n)) / 1_000_000_000;
            totalTime += elapsedTime;
            
            results.push({
                name: testName,
                passed: false,
                time: elapsedTime,
                error: error.message,
                error_type: error.name
            });
        }
    }
    
    // Imprimir resultados en JSON
    const finalResult = {
        tests: results,
        total_time: totalTime,
        passed: results.filter(r => r.passed).length,
        total: results.length
    };
    
    console.log(JSON.stringify(finalResult));
}

// Ejecutar tests
__runTests();
