package com.lab.orchestrator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class OrchestratorApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrchestratorApplication.class, args);
    }

    @RestController
    static class HealthController {
        @GetMapping("/health")
        public Object health() {
            return java.util.Map.of("ok", true, "service", "orchestrator-spring");
        }
    }
}
