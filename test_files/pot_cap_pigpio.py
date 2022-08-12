#!/usr/bin/env python

# pot_cap.py
# 2016-09-26
# Public Domain

import time
import pigpio

class reader:
   """
   A class to measure the time taken to charge a capacitor
   through a resistance.  The time taken will be propotional
   to the voltage, resistance, and capacitance.  If two values
   are fixed the third can be estimated.

   The following circuit should be used.

   3V3 ----- Resistor --+-- Capacitor ----- Ground
                        |
                        +-- GPIO

   """
   def __init__(self, pi, gpio, drain_ms=1.0, timeout_s=1.0):
      """
      Instantiate with the Pi and GPIO of the resistor/capacitor
      system to monitor.

      Optionally the time taken to fully drain the capacitor
      may be give as drain_ms.  The value defaults to
      1 millisecond.

      Optionally a timeout may be specified as timeout_s. The
      value defaults to 1.0 seconds.

      If the readings appear to vary too much in static
      conditions or there are many False results with massive
      readings perhaps the capacitor isn't fully discharging.
      Try increasing draim_ms.

      If False is always returned perhaps the capacitor needs
      more time to charge.  Try increasing timeout_s.
      """

      self.pi = pi
      self.gpio = gpio
      self.drain_ms = drain_ms
      self.timeout_s = timeout_s
      self._timeout_us = timeout_s * 1000000.0

      """
      Use a script on the daemon to do the time critical bit.

      It saves the tick in v0, changes the mode of p0 to an input,
      gets the tick and subtracts the first tick, divides by 2 to
      get the range, adds the range to the first tick to get the
      estimated start tick.  Returns the estimated start tick in p2
      and range in p3.  Finally p1 is incremented to indicate the
      script has completed.
      """

      self._sid = pi.store_script(
         b't sta v0 m p0 r t sub v0 div 2 sta p3 add v0 sta p2 inr p1 ')

      s = pigpio.PI_SCRIPT_INITING

      while s == pigpio.PI_SCRIPT_INITING:
         s, p = self.pi.script_status(self._sid)
         time.sleep(0.001)

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

   def _cbf(self, g, l, t):
      """
      Record the tick when the GPIO becomes high.
      """
      if l == 1:
         self._end = t

   def read(self):
      """
      Triggers and returns a reading.

      A tuple of the reading status (True for a good reading,
      False for a timeout or outlier), the reading, and the
      range are returned.

      The reading is the number of microseconds taken for the
      capacitor to charge.  The range is a measure of how
      accurately the start of recharge was measured as +/-
      microseconds.
      """

      timeout = time.time() + self.timeout_s

      self.pi.write(self.gpio, 0)

      time.sleep(self.drain_ms/1000.0)

      while (self.pi.read(self.gpio) != 0) and (time.time() < timeout):
         time.sleep(0.001)

      self._end = None

      self.pi.run_script(self._sid, [self.gpio, 0])

      while time.time() < timeout:
         s, p = self.pi.script_status(self._sid)
         if p[1]:
            break
         time.sleep(0.001)

      # p[2] is start charge tick from script
      # p[3] is +/- range from script

      if time.time() < timeout:

         _start = p[2]
         if _start < 0:
            _start += (1<<32)

         while self._end is None and time.time() < timeout:
            time.sleep(0.001)

         if self._end is not None:
            diff = pigpio.tickDiff(_start, self._end)
            # Discard obvious outliers
            if (diff < self._timeout_us) and (p[3] < 6):
               return True, diff, p[3]
            else:
               return False, diff, p[3]

      return False, 0, 0

   def cancel(self):
      """
      Cancels the reader and releases resources.
      """
      self.pi.delete_script(self._sid)
      self._cb.cancel()

if __name__ == "__main__":

   import sys
   import time
   import pigpio
   import pot_cap_pigpio as pot_cap

   RUN_TIME = 30
   POT_CAP_GPIO = 20
   DRAIN_MS = 1.0
   TIMEOUT_S = 1.0

   # ./pot_cap.py [run time [gpio [drain ms [timeout s]]]]

   if len(sys.argv) > 1:
      run_time = float(sys.argv[1])
   else:
      run_time = RUN_TIME

   if len(sys.argv) > 2:
      pot_cap_gpio = int(sys.argv[2])
   else:
      pot_cap_gpio = POT_CAP_GPIO

   if len(sys.argv) > 3:
      drain_ms = float(sys.argv[3])
   else:
      drain_ms = DRAIN_MS

   if len(sys.argv) > 4:
      timeout_s = float(sys.argv[4])
   else:
      timeout_s = TIMEOUT_S

   pi = pigpio.pi() # Connect to Pi.

   print("# rt={:.1f} g={} drain={:.1f} timeout={:.1f}".format(
      run_time, pot_cap_gpio, drain_ms, timeout_s))

   # Instantiate Pot/Cap reader.
   pc = pot_cap.reader(pi, pot_cap_gpio, drain_ms, timeout_s)
   
   start = time.time()

   while (time.time()-start) < run_time:

      s, v, r = pc.read()
      print("{} {} {}".format(s, v, r))
      time.sleep(0.01)

   pc.cancel() # Cancel the reader.
   pi.stop()   # Disconnect from Pi.

