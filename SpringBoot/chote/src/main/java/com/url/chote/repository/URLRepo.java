package com.url.chote.repository;

import com.url.chote.model.URLMapper;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface URLRepo extends JpaRepository<URLMapper, String> {
}
