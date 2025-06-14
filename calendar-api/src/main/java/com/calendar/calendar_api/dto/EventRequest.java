package com.calendar.calendar_api.dto;

public class EventRequest {

    private String summary;
    private String description;
    private String location;
    private String startDateTime; // Ex: "2025-06-15T10:00:00-03:00"
    private String endDateTime;   // Ex: "2025-06-15T11:00:00-03:00"

    // Getters e Setters
    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getStartDateTime() {
        return startDateTime;
    }

    public void setStartDateTime(String startDateTime) {
        this.startDateTime = startDateTime;
    }

    public String getEndDateTime() {
        return endDateTime;
    }

    public void setEndDateTime(String endDateTime) {
        this.endDateTime = endDateTime;
    }

}

