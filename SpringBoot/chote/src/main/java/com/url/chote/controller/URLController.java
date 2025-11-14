package com.url.chote.controller;

import com.url.chote.service.URLService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
@CrossOrigin(origins = "*")
public class URLController {

    @Autowired
    private URLService urlService;

    @GetMapping
    public String home(){
        return "index.html";
    }

    @PostMapping
    @ResponseBody
    public String add(@RequestParam String longUrl, @RequestParam(required = false) String shortUrl ){
        return urlService.add(longUrl, shortUrl);
    }

    @GetMapping("/{scode:[A-Za-z0-9_-]+}")
    public String redirect(@PathVariable String scode){
        return  "redirect:"+urlService.redirectFrom(scode);
    }

}
