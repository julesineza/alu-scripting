#!/usr/bin/env ruby
input = ARGV[0]
from  = input.scan(/\[from:(.*?)\]/).join
to    = input.scan(/\[to:(.*?)\]/).join
flags = input.scan(/\[flags:(.*?)\]/).join
puts "#{from},#{to},#{flags}"