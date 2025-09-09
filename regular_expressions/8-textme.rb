#!/usr/bin/env ruby
log = ARGV[0]

regex = /\[from:(.*?)\].*?\[to:(.*?)\].*?\[flags:(.*?)\]/
match = log.match(regex)

if match
  sender, receiver, flags = match.captures
  puts "#{sender},#{receiver},#{flags}"
end
