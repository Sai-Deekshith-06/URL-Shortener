package com.url.chote.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;

@Entity
@Table(name = "urls",
        uniqueConstraints = @UniqueConstraint(columnNames = "shortUrl"))
@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class URLMapper {

    @Id
    @Column(length = 10, nullable = false, unique = true)
    private String shortUrl;

    @Column(nullable = false)
    private String longUrl;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;
}
