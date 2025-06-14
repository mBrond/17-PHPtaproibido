package com.calendar.calendar_api.service;

import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.client.util.DateTime;
import com.google.api.services.calendar.Calendar;
import com.google.api.services.calendar.CalendarScopes;
import com.google.api.services.calendar.model.Event;
import com.google.api.services.calendar.model.EventDateTime;
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;
import com.calendar.calendar_api.dto.EventRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.security.GeneralSecurityException;
import java.util.Collections;

@Service
public class CalendarService {

    private static final String APPLICATION_NAME = "Spring Boot Calendar API";
    private static final String CREDENTIALS_FILE_PATH = "/credentials.json";

    @Value("${google.calendar.id}")
    private String calendarId;

    public String createEvent(EventRequest eventRequest) throws GeneralSecurityException, IOException {
        // 1. Autenticação (igual a antes)
        InputStream in = CalendarService.class.getResourceAsStream(CREDENTIALS_FILE_PATH);
        GoogleCredentials credentials = GoogleCredentials.fromStream(in)
                .createScoped(Collections.singleton(CalendarScopes.CALENDAR));

        // 2. Construir o serviço do Calendar
        Calendar service = new Calendar.Builder(
                GoogleNetHttpTransport.newTrustedTransport(),
                GsonFactory.getDefaultInstance(),
                new HttpCredentialsAdapter(credentials))
                .setApplicationName(APPLICATION_NAME)
                .build();

        // 3. Criar o objeto do Evento a partir do DTO
        Event event = new Event()
                .setSummary(eventRequest.getSummary())
                .setLocation(eventRequest.getLocation())
                .setDescription(eventRequest.getDescription());

        DateTime startDateTime = new DateTime(eventRequest.getStartDateTime());
        EventDateTime start = new EventDateTime().setDateTime(startDateTime).setTimeZone("America/Sao_Paulo");
        event.setStart(start);

        DateTime endDateTime = new DateTime(eventRequest.getEndDateTime());
        EventDateTime end = new EventDateTime().setDateTime(endDateTime).setTimeZone("America/Sao_Paulo");
        event.setEnd(end);

        // 4. Inserir o evento no calendário
        Event createdEvent = service.events().insert(calendarId, event).execute();

        return createdEvent.getHtmlLink();
    }
}
