#!/usr/bin/env fish
function pass
  echo "PASS" 
  exit 0
end

function fail
  echo "FAIL with $argv or 1" 
  if test (count $argv) -eq 0; or test (math $argv[1]) -le 0
      exit 1
  else
     exit $argv[1]
  end
end

function stock
    set -l secs (test (math $argv[1]) -gt 0; and echo $argv[1]; or echo 6)
    echo "STOCKING with timeout $secs"
    sleep $secs
end

function help
    echo "example.fish success|fail (exit status)| stock (timeout)"
end


eval $argv
