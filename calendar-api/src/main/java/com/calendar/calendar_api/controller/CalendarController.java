package com.calendar.calendar_api.controller;

import com.calendar.calendar_api.dto.EventRequest;
import com.calendar.calendar_api.service.CalendarService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/events")
public class CalendarController {

    @Autowired
    private CalendarService calendarService;

    @PostMapping
    public ResponseEntity<String> createEvent(@RequestBody EventRequest eventRequest) {
        System.out.println("recebemos algo");
        try {
            String eventLink = calendarService.createEvent(eventRequest);
            return ResponseEntity.ok("Evento criado com sucesso! Link: " + eventLink);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("Erro ao criar o evento: " + e.getMessage());
        }
    }
}
