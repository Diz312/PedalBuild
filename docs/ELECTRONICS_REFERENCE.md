# Electronics Reference for Guitar Pedal Building

This document provides domain knowledge for developing PedalBuild's schematic analysis, BOM validation, and breadboard layout agents.

## Purpose

This reference informs the implementation of:
- **Schematic Analyzer Agent** (Google ADK) - Multi-pass vision analysis
- **BOM Manager Service** - Component matching and validation
- **Breadboard Layout Agent** (Google ADK) - Optimal layout generation
- **Component Inventory Service** - Stock tracking and categorization

---

## 1. Electronic Components

### Resistors

**Values**: Use ohm notation (10k = 10,000Ω, 1M = 1,000,000Ω)

**Common Values** (E12 series): 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82 (with multipliers: ×10, ×100, ×1k, ×10k, ×100k, ×1M)

**Power Ratings**: 1/4W (most common in pedals), 1/2W, 1W

**Tolerances**: 5% (gold band), 1% (brown band)

**Schematic Symbols**:
- US: Zigzag line
- EU: Rectangle

**Reference Designators**: R1, R2, R3...

### Capacitors

**Types**:
- **Ceramic**: Non-polarized, small values (1pF - 1µF), cheap, can be microphonic
- **Film**: Non-polarized, better audio quality, larger physically, 1nF - 1µF range
- **Electrolytic**: Polarized (+/-), large values (1µF - 1000µF), power supply filtering

**Value Notation**:
- pF (picofarads): 1-999pF
- nF (nanofarads): 1nF = 1000pF, common: 1n, 10n, 100n, 220n, 470n
- µF (microfarads): 1µF = 1000nF, common: 1µ, 10µ, 100µ, 220µ, 470µ

**Voltage Ratings**: 16V, 25V, 50V, 100V (pedals typically use 16V minimum for 9V circuits)

**Schematic Symbols**:
- Non-polarized: Two parallel lines
- Polarized (electrolytic): One straight line, one curved line (curved = negative)

**Reference Designators**: C1, C2, C3...

### Transistors

**Types**:
- **BJT (Bipolar Junction Transistor)**: NPN or PNP
- **JFET (Junction Field-Effect Transistor)**: N-channel or P-channel
- **MOSFET (Metal-Oxide-Semiconductor FET)**: N-channel or P-channel

**Common BJTs in Pedals**:
- **2N3904** (NPN): General purpose, hFE ~100-300
- **2N5088** (NPN): High gain, hFE ~400-800, used in Big Muff, Rat
- **BC549** (NPN): Low noise, similar to 2N3904
- **2N3906** (PNP): Complement to 2N3904
- **2N5087** (PNP): High gain, complement to 2N5088
- **BC559** (PNP): Complement to BC549

**Common JFETs**:
- **J201** (N-channel): High gain, used in input buffers
- **2N5457** (N-channel): Lower gain

**Package**: TO-92 (most common for through-hole)

**Pinout (TO-92)**: Varies by part! Common patterns:
- 2N3904: E-B-C (flat side facing you, left to right)
- 2N5088: E-B-C (same as 2N3904)
- BC549: C-B-E (different!)

**Schematic Symbol**:
- NPN: Arrow pointing OUT from base
- PNP: Arrow pointing IN to base

**Reference Designators**: Q1, Q2, Q3...

### Op-Amps (Operational Amplifiers)

**Common Op-Amps in Pedals**:
- **TL072**: Dual JFET-input, low noise, "transparent" sound, very common
- **TL082**: Similar to TL072, slightly higher slew rate
- **JRC4558**: Dual BJT-input, "warmer" sound, classic Tube Screamer chip
- **LM358**: Dual, single-supply friendly, cheaper
- **LM308**: Single op-amp, used in ProCo RAT
- **NE5532**: Dual, low noise, high performance

**Package**: DIP-8 (breadboard friendly)

**Pinout (DIP-8, dual op-amp)**:
```
    TL072 / JRC4558 / NE5532
    ┌─────┬─────┐
    │1 OUT A    8│ V+
    │2 IN- A    7│ OUT B
    │3 IN+ A    6│ IN- B
    │4 V-       5│ IN+ B
    └───────────┘
```

**Supply Voltage**:
- Dual supply: ±9V (V+ = +9V, V- = -9V, ground in middle)
- Single supply: 9V (V+ = +9V, V- = ground, virtual ground at 4.5V)

**Reference Designators**: IC1, IC2, IC3...

### Diodes

**Common Diodes in Pedals**:
- **1N4148**: Signal diode, fast switching, used for clipping
- **1N914**: Equivalent to 1N4148
- **1N4001-1N4007**: Rectifier diodes, reverse polarity protection
- **1N5817**: Schottky diode, lower voltage drop
- **1N34A**: Germanium diode, "softer" clipping
- **LED (Light Emitting Diode)**: Red, green, blue, indicator + clipping

**Polarity**: Anode (+) to Cathode (-), band marks cathode

**Schematic Symbol**: Triangle pointing to bar (bar = cathode)

**Reference Designators**: D1, D2, D3...

### Potentiometers

**Taper Types**:
- **Linear (B-taper)**: Resistance changes linearly with rotation, used for tone controls
- **Audio/Log (A-taper)**: Logarithmic curve, used for volume controls (matches human hearing)

**Common Values**: 10k, 25k, 50k, 100k, 500k, 1M

**Mounting**: PCB-mount vs panel-mount (breadboard uses wires to off-board pot)

**Pins**: 3 pins (left, wiper/center, right)

**Reference Designators**: VR1, VR2, VR3... or POT1, POT2...

### Integrated Circuits (Special)

**PT2399**: Digital delay IC, cheap, 340ms max delay
**MN3207**: Analog BBD (Bucket Brigade Device) for chorus/flanger
**CD4049**: CMOS hex inverter, used for gain stages in some pedals
**LM7809**: 9V voltage regulator
**TC1044**: Charge pump for generating -9V from +9V

---

## 2. Schematic Conventions

### Symbol Recognition

**Critical**: Components can be oriented **vertically OR horizontally** in schematics.

**Common Symbols**:
- **Resistor**: Zigzag (US) or rectangle (EU)
- **Capacitor**: Two parallel lines (non-polar) or line + curve (polarized)
- **Transistor**: Circle with 3 lines (collector, base, emitter), arrow indicates type
- **Op-Amp**: Triangle with inputs on left (+/-), output on right
- **Diode**: Triangle pointing to bar
- **Ground**: Three descending lines or earth symbol
- **Power**: Arrow up or labeled (VCC, V+, +9V)

### Reference Designators

Standard prefixes:
- R = Resistor
- C = Capacitor
- Q = Transistor
- IC = Integrated Circuit
- D = Diode
- VR/POT = Potentiometer
- J = Jack (input/output)
- SW = Switch

Numbered sequentially: R1, R2, R3, C1, C2, C3...

### Net Labels

Common labels:
- **VCC / V+ / +9V**: Positive power supply
- **GND**: Ground (0V reference)
- **V-**: Negative supply (in dual supply circuits)
- **VREF / VB**: Virtual ground (4.5V in single supply)
- **INPUT / IN**: Audio input
- **OUTPUT / OUT**: Audio output
- **DRIVE, TONE, VOLUME**: Control signals to potentiometers

### Multi-Sheet Schematics

Large circuits may span multiple pages with:
- **Off-page connectors**: Show signal going to another page
- **Hierarchical blocks**: Sub-circuits represented as blocks
- **Power/Ground**: Not always shown on every component (implied)

---

## 3. Guitar Pedal Circuit Topology

### Input Stage

**Purpose**: Buffer guitar signal (high impedance ~1MΩ)

**Implementations**:
- **Op-amp buffer**: Non-inverting amplifier with gain = 1
- **JFET buffer**: Using J201 or similar
- **BJT buffer**: Emitter follower

### Gain Stages

**Purpose**: Amplify signal and add harmonic distortion

**Types**:
- **Non-inverting op-amp**: Gain set by feedback resistors
- **Inverting op-amp**: Inverts phase, different frequency response
- **Transistor common-emitter**: Classic gain stage

**Clipping**:
- **Hard clipping**: Diodes to ground after gain stage (Tube Screamer, RAT)
- **Soft clipping**: Diodes in feedback loop (Klon, Blues Driver)
- **No clipping**: Clean boost (op-amp without clipping diodes)

### Tone Control

**Types**:
- **Passive Big Muff stack**: Simple RC filters, scooped mids
- **Active Baxandall**: Bass and treble controls using op-amp
- **Fixed**: Single capacitor to ground (simple high-pass filter)

### Output Stage

**Purpose**: Provide low impedance output, volume control

**Implementation**:
- **Buffer after volume pot**: Prevents loading by guitar amp
- **Volume pot**: 100k or higher value

### Power Supply

**9V Battery or DC Jack**:
- **Reverse polarity protection**: Diode or MOSFET
- **Filtering**: 100µF electrolytic + 100nF ceramic
- **Virtual ground** (single supply): Voltage divider + buffer to 4.5V

**Dual Supply** (less common):
- **Charge pump**: TC1044 or MAX1044 generates -9V from +9V
- **Benefits**: More headroom, symmetrical clipping

---

## 4. Breadboard Layout Principles

### Signal Flow

**Convention**: Left (input) to right (output)

**Stages**:
1. Input buffer (left side)
2. Gain/clipping stages (center)
3. Tone control (center-right)
4. Output buffer (right side)

### Power Distribution

**Use Power Rails**: Top and bottom rails on breadboard

**Decoupling**: 100nF ceramic capacitor between V+ and GND near each IC

**Bulk Filtering**: 100µF electrolytic at power input

### Grounding

**Star Ground**: All grounds meet at single point (minimizes ground loops)

**Single-Point Ground**: Connect ground rail to input jack ground only

**Avoid Ground Loops**: Don't create multiple ground paths

### Component Placement

**ICs**: Straddle center trough of breadboard (pins on opposite sides)

**Decoupling Caps**: Place 100nF ceramic immediately adjacent to IC power pins

**Potentiometers**: External, connect via jumper wires to breadboard edge

**Audio Jacks**: External, use short wires to breadboard

**Through-Hole**: Insert components fully, trim leads

### Wire Routing

**Signal Wires**: Keep short, avoid long runs

**Power Wires**: Separate from signal wires to reduce noise

**Wire Colors** (convention):
- **Red**: Positive voltage (+9V, +4.5V)
- **Black**: Ground (GND)
- **Yellow/White**: Signal (audio)
- **Blue**: Negative voltage (-9V if dual supply)

**Minimize Crossings**: Plan layout to reduce wire crossings

### Noise Reduction

**High-Gain Circuits**: Extra attention to grounding and decoupling

**Shielded Cable**: Use for input/output connections (breadboard testing)

**Separation**: Keep noisy sections (power supply, digital) away from sensitive (input buffer)

---

## 5. Component Substitution Rules

### Op-Amps

**Pin-Compatible** (DIP-8 dual op-amps):
- TL072 ↔ TL082 ↔ JRC4558 ↔ NE5532 ↔ LM358

**Sound Differences**:
- TL072: "Transparent", low noise
- JRC4558: "Warm", slightly colored, classic Tube Screamer sound
- NE5532: High performance, low noise, slightly "brighter"

**Substitution Rule**: Usually safe to swap, but may affect tone slightly

### Transistors (BJT)

**NPN Substitutes** (similar gain):
- 2N3904 ↔ 2N5088 ↔ BC549 ↔ 2N2222

**Gain Differences**:
- 2N3904: hFE ~100-300
- 2N5088: hFE ~400-800 (higher gain, more distortion)

**Substitution Rule**: Check pinout (EBC vs CBE)! Gain affects tone in fuzz circuits.

**PNP Complements**:
- 2N3904 (NPN) ↔ 2N3906 (PNP)
- 2N5088 (NPN) ↔ 2N5087 (PNP)

### Capacitors

**Ceramic ↔ Film**:
- Sound difference: Film is "warmer", ceramic can be "harsh" or microphonic
- Recommendation: Use film in signal path, ceramic for power decoupling

**Electrolytic ↔ Film**:
- Electrolytic: Large values (>1µF), polarized
- Film: Small values (<1µF), non-polarized
- Substitution: Cannot substitute electrolytic with film in same size/value

### Diodes

**Signal Diodes**:
- 1N4148 ↔ 1N914 (equivalent)

**Clipping Diodes** (tone differences):
- Silicon (1N4148): Hard, asymmetric clipping
- Germanium (1N34A): Soft, symmetric clipping
- LED: Higher forward voltage, more headroom

**Substitution Rule**: Different diode types = different clipping characteristics

### Resistors

**Any resistor type works**: Carbon film, metal film, carbon composition

**Tolerance**: 5% tolerance is fine for audio (1% not necessary)

**Power Rating**: 1/4W sufficient for most pedal resistors

**Substitution Rule**: Freely substitute, no audible difference

---

## 6. Common Guitar Pedal Circuits

### Tube Screamer (Overdrive)

**Topology**:
- Input buffer (op-amp)
- Non-inverting gain stage with diodes in feedback loop (soft clipping)
- Active tone control (variable low-pass filter)
- Output buffer

**Key Components**:
- IC: JRC4558 (or TL072)
- Clipping diodes: 1N4148 (silicon)
- Tone cap: 0.22µF

**Schematic Recognition**: Diodes in op-amp feedback loop

### ProCo RAT (Distortion)

**Topology**:
- Input buffer
- LM308 op-amp gain stage (very high gain)
- Variable low-pass filter (Filter control)
- Hard clipping with diodes to ground
- Output buffer

**Key Components**:
- IC: LM308 (single op-amp)
- Clipping diodes: 1N4148 or LED
- Filter cap: 47pF (negative feedback)

**Schematic Recognition**: LM308 with 47pF cap in feedback

### Big Muff (Fuzz)

**Topology**:
- Input buffer
- 2 transistor gain stages with diode clipping
- Passive tone stack (Big Muff tone stack)
- Output buffer

**Key Components**:
- Transistors: 2N5088 or BC549 (4 total)
- Clipping diodes: 1N4148
- Tone caps: 0.01µF, 0.004µF (classic Muff values)

**Schematic Recognition**: 4 transistors in cascade, passive tone stack

### PT2399 Delay

**Topology**:
- Input buffer
- PT2399 digital delay IC
- Feedback loop (repeats)
- Wet/dry mix
- Output buffer

**Key Components**:
- IC: PT2399 (16-pin DIP)
- Clock resistor: Sets delay time (100k-330k)
- Filtering: Low-pass filters to remove aliasing

**Schematic Recognition**: PT2399 chip (distinctive pinout)

---

## 7. PedalBuild Application Context

### For Schematic Analyzer Agent

**Multi-Pass Vision Analysis**:
1. **Pass 1**: Identify all component symbols (R, C, Q, IC, D)
2. **Pass 2**: Extract values and reference designators
3. **Pass 3**: Map connections (netlist)

**Orientation Handling**: Check BOTH vertical and horizontal orientations

**Confidence Scoring**: Flag components with confidence < 0.7 for user review

**Output**: JSON with components, values, connections, confidence scores

### For BOM Manager Service

**Component Matching**:
- Fuzzy matching: "10k" = "10K" = "10000" = "10kΩ"
- Type matching: Resistor, capacitor, transistor, IC, diode
- Package matching: DIP-8, TO-92, 1/4W

**Substitution Logic**:
- Check substitution rules (op-amps, transistors)
- Flag substitutions for user approval
- Document tone differences

**Inventory Validation**:
- Check stock quantity
- Identify missing components
- Suggest alternatives from inventory

### For Breadboard Layout Agent

**Dual-Board Platform** (per user requirements):
- 2 breadboards side-by-side
- Per board: 2 power rails + (a-j rows × 63 columns) + through-hole + (a-j rows × 63 columns) + 2 power rails
- Built-in jumper banks: INPUT, GND, 3.3V, REF, 5V, 9V, -9V, 18V, OUTPUT
- 6 potentiometer slots at top
- 2× 1/4" jacks + effect bypass switch

**Layout Optimization**:
- Place ICs straddling center trough
- Group by function (power, signal, output)
- Minimize wire crossings
- Use power rails efficiently
- Consider signal flow left-to-right

**Output Formats**:
- Fritzing (.fzz) file - editable layout
- PNG image - visual reference

### For Component Inventory Service

**Categorization**:
- Type: Resistor, capacitor, transistor, IC, diode, potentiometer
- Value: Parsed numeric value (10k = 10000)
- Package: DIP-8, TO-92, 1/4W, etc.
- Location: Drawer/bin organization

**Stock Tracking**:
- Quantity on hand
- Low stock alerts (< threshold)
- Flag duplicates

---

## 8. Development Guidelines

### When Implementing Agents

**Use this reference for**:
- Component symbol recognition in schematic vision analysis
- Component value parsing (10k → 10000)
- Substitution rule logic in BOM validation
- Layout placement algorithms
- Component categorization in inventory

**Context Engineering**:
- Each Google ADK agent should have a `context.md` file
- Include relevant sections from this reference
- Keep context focused on agent's specific task

**Tool Descriptions**:
- Be specific: "Parse resistor value '10k' to 10000 ohms"
- Include examples: "TL072 has pins: 1=OUT1, 2=IN1-, 3=IN1+, 4=V-, ..."
- Mention edge cases: "Capacitor can be pF, nF, or µF - handle all notations"

### Testing with Real Circuits

**Use these schematics for testing**:
- Tube Screamer (TS808) - Classic overdrive
- ProCo RAT - High-gain distortion
- Electro-Harmonix Big Muff - 4-transistor fuzz
- Boss DS-1 - Simple distortion
- MXR Phase 90 - 4-stage phaser

**Available at**: PedalPCB.com, Electro-Smash, DIYStompboxes

---

## 9. Sources and Further Reading

### Datasheets
- TI TL072: https://www.ti.com/product/TL072
- ON Semi 2N3904: https://www.onsemi.com/products/discretes-drivers/transistors/2n3904

### Guitar Pedal Resources
- **Electro-Smash**: https://www.electrosmash.com/ (detailed pedal analysis)
- **DIYStompboxes**: https://www.diystompboxes.com/smfforum/ (forum)
- **PedalPCB**: https://www.pedalpcb.com/ (build docs, schematics)
- **Tagboard Effects**: http://tagboardeffects.blogspot.com/ (layouts)

### Books
- "The Art of Electronics" - Horowitz & Hill
- "DIY Guitar Effects Pedals" - Brian Wampler
- "Designing Tube Preamps for Guitar and Bass" - Merlin Blencowe

### Electronics Fundamentals
- **All About Circuits**: https://www.allaboutcircuits.com/
- **Electronics Tutorials**: https://www.electronics-tutorials.ws/

---

**Last Updated**: 2026-02-14

**See Also**:
- [CLAUDE.md](../CLAUDE.md) - Project-specific guidelines
- [Implementation Plan](../.claude/plans/sunny-stargazing-garden.md) - Phase 1-6 plan
- [CLAUDE_CODE_TOOLS.md](../CLAUDE_CODE_TOOLS.md) - Development tools
