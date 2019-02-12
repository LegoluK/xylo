ON_IMG = on.jpg
ON_RESIZED_IMG = on_resized.jpg
OUT_IMG = out.jpg
SCRIPT = led.py

display: $(OUT_IMG)
	display $<

$(OUT_IMG): $(SCRIPT) $(ON_RESIZED_IMG)
	./$(SCRIPT) $(ON_RESIZED_IMG) $(OUT_IMG)

$(ON_RESIZED_IMG): $(ON_IMG)
	convert $< -resize 640x480 $@

clean:
	rm $(ON_RESIZED_IMG) $(OUT_IMG)
