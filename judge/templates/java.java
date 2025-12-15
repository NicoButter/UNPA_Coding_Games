"""
Plantilla de ejecución para Java
Combina el código del usuario con los tests ocultos
"""
import com.google.gson.Gson;
import java.util.*;
import java.io.*;

// CÓDIGO DEL USUARIO
{user_code}

// CLASE DE TESTING
class __JudgeRunner {
    static class TestCase {
        String name;
        String input;
        String expected;
        Map<String, Object> function_call;
        
        public TestCase() {}
    }
    
    static class TestResult {
        String name;
        boolean passed;
        double time;
        String expected;
        String actual;
        String error;
        String error_type;
        
        public TestResult() {}
    }
    
    static class FinalResult {
        List<TestResult> tests;
        double total_time;
        int passed;
        int total;
        
        public FinalResult() {
            tests = new ArrayList<>();
        }
    }
    
    public static void main(String[] args) {
        try {
            String testsJson = "{tests_json}";
            Gson gson = new Gson();
            TestCase[] tests = gson.fromJson(testsJson, TestCase[].class);
            
            FinalResult finalResult = new FinalResult();
            double totalTime = 0;
            
            for (int i = 0; i < tests.length; i++) {
                TestCase test = tests[i];
                TestResult result = new TestResult();
                result.name = test.name != null ? test.name : "Test " + (i + 1);
                
                try {
                    // Preparar entrada si existe
                    if (test.input != null && !test.input.isEmpty()) {
                        System.setIn(new ByteArrayInputStream(test.input.getBytes()));
                    }
                    
                    // Capturar salida
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    PrintStream ps = new PrintStream(baos);
                    PrintStream old = System.out;
                    System.setOut(ps);
                    
                    // Medir tiempo
                    long startTime = System.nanoTime();
                    
                    // Ejecutar función del usuario o código principal
                    String actualOutput = "";
                    if (test.function_call != null) {
                        // Aquí habría que usar reflection para llamar a la función
                        // Por simplicidad, asumimos que hay un método solve() público
                        actualOutput = Solution.solve(test.input);
                    } else {
                        // Ejecutar main del usuario
                        Solution.main(new String[]{});
                        actualOutput = baos.toString().trim();
                    }
                    
                    double elapsedTime = (System.nanoTime() - startTime) / 1_000_000_000.0;
                    totalTime += elapsedTime;
                    
                    // Restaurar stdout
                    System.out.flush();
                    System.setOut(old);
                    
                    // Comparar salidas
                    String expected = test.expected != null ? test.expected.trim() : "";
                    result.passed = actualOutput.equals(expected);
                    result.time = elapsedTime;
                    result.expected = expected;
                    result.actual = actualOutput;
                    
                } catch (Exception e) {
                    long elapsedTime = (System.nanoTime() - System.currentTimeMillis() * 1_000_000) / 1_000_000_000;
                    result.passed = false;
                    result.time = elapsedTime;
                    result.error = e.getMessage();
                    result.error_type = e.getClass().getSimpleName();
                    System.setOut(System.out);
                }
                
                finalResult.tests.add(result);
            }
            
            finalResult.total_time = totalTime;
            finalResult.passed = (int) finalResult.tests.stream().filter(r -> r.passed).count();
            finalResult.total = tests.length;
            
            // Imprimir resultados en JSON
            System.out.println(gson.toJson(finalResult));
            
        } catch (Exception e) {
            System.err.println("Error en el runner: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
