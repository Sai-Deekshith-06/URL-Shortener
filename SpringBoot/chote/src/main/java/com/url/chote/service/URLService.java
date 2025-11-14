package com.url.chote.service;

import com.url.chote.model.URLMapper;
import com.url.chote.repository.URLRepo;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.security.SecureRandom;
import java.time.Duration;
import java.time.Instant;

@Service
public class URLService {
    @Autowired
    private URLRepo db;

    private static final String CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-";
    private static final SecureRandom RANDOM = new SecureRandom();

    private String generateUniqueId() {
        StringBuilder sb = new StringBuilder(6);
        do {
            sb.setLength(0);
            for (int i = 0; i < 6; i++) {
                sb.append(CHARSET.charAt(RANDOM.nextInt(CHARSET.length())));
            }
        } while (db.existsById(sb.toString()));
        return sb.toString();
    }

    public boolean isFree(String shortUrl) {
        return db.findById(shortUrl)
                .map(existing -> {

                    Instant expiresAt = existing.getCreatedAt().plus(Duration.ofMinutes(2));
                    boolean expired = Instant.now().isAfter(expiresAt);

                    if (expired) {
                        db.deleteById(shortUrl);
                        db.flush();
                        return true;
                    }

                    return false;
                })
                .orElse(true);
    }

    @Transactional
    public String add(String longUrl, String shortUrl) {

        if (shortUrl == null || shortUrl.isBlank())
            shortUrl = generateUniqueId();
        else if (!isFree(shortUrl))
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "oops..!! URL already exists, try another combination");

        URLMapper newUrl = URLMapper.builder()
                .shortUrl(shortUrl)
                .longUrl(longUrl)
                .createdAt(Instant.now())
                .build();

        db.saveAndFlush(newUrl);
        return shortUrl;
    }

    public String redirectFrom(String shortUrl) {
        return !isFree(shortUrl) ? db.findById(shortUrl).get().getLongUrl() : "/?shortUrl=" + shortUrl;
    }

}
