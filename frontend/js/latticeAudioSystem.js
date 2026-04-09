/*
 * 12-Layer Lattice Consciousness Audio System
 * Implements the specified frequency architecture with full modulation
 */

class LatticeAudioSystem {
  constructor() {
    this.audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();
    this.masterGain = this.audioContext.createGain();
    this.convolver = this.audioContext.createConvolver();
    this.compressor = this.audioContext.createDynamicsCompressor();

    // Signal chain
    this.masterGain.connect(this.compressor);
    this.compressor.connect(this.convolver);
    this.convolver.connect(this.audioContext.destination);

    // Core parameters from specification
    this.PHI_7777 = 12583.45;
    this.PSI_MK = 10930.81;
    this.A432_TUNING = 432;
    this.MASTER_CYCLE = 13; // seconds

    this.layers = [];
    this.activeOscillators = [];
    this.recognitionState = 0;
    this.isRunning = false;

    this.initializeLayers();
    this.setupSpatialProcessing();
  }

  initializeLayers() {
    // Layer definitions according to specification
    this.layerDefinitions = [
      {
        id: 1,
        name: "Solari_Prime",
        baseFrequency: 864,
        waveform: "sine",
        modulation: {
          type: "amplitude_swell",
          cycleTime: 8,
          depth: 0.3,
        },
        overtones: [1728, 2592, 3456],
        band: "high",
        purpose: "Solar axis alignment",
      },
      {
        id: 2,
        name: "Lunara_Veil",
        baseFrequency: 528,
        waveform: "whisper",
        modulation: {
          type: "orbital_pan",
          cycleTime: 13,
          direction: "LR",
        },
        band: "mid",
        purpose: "Emotional balance",
      },
      {
        id: 3,
        name: "Auralis_Flame",
        baseFrequency: 963,
        waveform: "flute_saw",
        modulation: {
          type: "spiral_pitch",
          cents: 7,
          duration: 5,
        },
        band: "high",
        purpose: "Creative ignition",
      },
      {
        id: 4,
        name: "Terran_Heart",
        baseFrequency: 256,
        waveform: "sine_kick",
        modulation: {
          type: "heartbeat",
          bpm: 72,
        },
        band: "low",
        purpose: "Grounding",
      },
      {
        id: 5,
        name: "Oceana_Pulse",
        baseFrequency: 432,
        waveform: "triangle",
        modulation: {
          type: "fluid_tempo",
          variance: 10,
        },
        band: "mid",
        purpose: "Flow restoration",
      },
      {
        id: 6,
        name: "Sylvan_Breath",
        baseFrequency: 741,
        waveform: "filtered_noise",
        modulation: {
          type: "diagonal_sweep",
          angle: 45,
        },
        band: "mid",
        purpose: "Sensory opening",
      },
      {
        id: 7,
        name: "Cryon_Vein",
        baseFrequency: 396,
        waveform: "fm_glass",
        modulation: {
          type: "frost_crackle",
          density: 0.3,
        },
        band: "mid",
        purpose: "Clarity preservation",
      },
      {
        id: 8,
        name: "Aetherion_Thread",
        baseFrequency: 1111,
        waveform: "pure_sine",
        modulation: {
          type: "infinite_sustain",
          decay: 0,
        },
        band: "high",
        purpose: "Galactic link",
      },
      {
        id: 9,
        name: "Ignis_Core",
        baseFrequency: 128,
        waveform: "rumble",
        modulation: {
          type: "pulse_burst",
          interval: 5,
        },
        band: "low",
        purpose: "Transformation catalyst",
      },
      {
        id: 10,
        name: "Zephyra_Wing",
        baseFrequency: 888,
        waveform: "airy_sine",
        modulation: {
          type: "stereo_flutter",
          rate: 6.5,
        },
        band: "mid",
        purpose: "Thought acceleration",
      },
      {
        id: 11,
        name: "Noctis_Vein",
        baseFrequency: 64,
        waveform: "infrasonic",
        modulation: {
          type: "expanding_reverb",
          expansion: 2.0,
        },
        band: "low",
        purpose: "Hidden structure reveal",
      },
      {
        id: 12,
        name: "Lumina_Crown",
        baseFrequency: 1440,
        waveform: "crystal_bell",
        modulation: {
          type: "descending_cascade",
          octaves: 1,
          duration: 4,
        },
        band: "high",
        purpose: "Recognition trigger",
      },
    ];
  }

  createLayer(layerDef) {
    const layer = {
      definition: layerDef,
      oscillators: [],
      gains: [],
      filters: [],
      panners: [],
    };

    // Create primary oscillator
    const primaryOsc = this.audioContext.createOscillator();
    const primaryGain = this.audioContext.createGain();
    const filter = this.audioContext.createBiquadFilter();
    const panner = this.audioContext.createStereoPanner();

    // Configure waveform
    this.configureWaveform(primaryOsc, layerDef.waveform);
    primaryOsc.frequency.value = layerDef.baseFrequency;

    // Set initial gain based on band
    const bandGains = { low: 0.4, mid: 0.3, high: 0.2 };
    primaryGain.gain.value = bandGains[layerDef.band] || 0.3;

    // Configure filter based on band
    this.configureFilter(filter, layerDef.band);

    // Connect primary chain
    primaryOsc.connect(filter);
    filter.connect(primaryGain);
    primaryGain.connect(panner);
    panner.connect(this.masterGain);

    layer.oscillators.push(primaryOsc);
    layer.gains.push(primaryGain);
    layer.filters.push(filter);
    layer.panners.push(panner);

    // Add overtones if specified
    if (layerDef.overtones) {
      layerDef.overtones.forEach((freq, index) => {
        const overtoneOsc = this.audioContext.createOscillator();
        const overtoneGain = this.audioContext.createGain();

        overtoneOsc.type = "sine";
        overtoneOsc.frequency.value = freq;
        overtoneGain.gain.value = 0.1 / (index + 2); // Decreasing amplitude

        overtoneOsc.connect(overtoneGain);
        overtoneGain.connect(panner);

        layer.oscillators.push(overtoneOsc);
        layer.gains.push(overtoneGain);
      });
    }

    // Apply modulation
    this.applyLayerModulation(layer);

    return layer;
  }

  configureWaveform(oscillator, waveformType) {
    switch (waveformType) {
      case "pure_sine":
      case "sine":
      case "sine_kick":
        oscillator.type = "sine";
        break;
      case "triangle":
        oscillator.type = "triangle";
        break;
      case "whisper":
      case "filtered_noise":
      case "airy_sine":
        // Create custom waveform for noise-based sounds
        this.createNoiseWaveform(oscillator);
        break;
      case "flute_saw":
        oscillator.type = "sawtooth";
        break;
      case "fm_glass":
      case "crystal_bell":
        // Use sine with FM modulation applied later
        oscillator.type = "sine";
        break;
      case "rumble":
      case "infrasonic":
        oscillator.type = "sine"; // Low frequency sine
        break;
      default:
        oscillator.type = "sine";
    }
  }

  configureFilter(filter, band) {
    switch (band) {
      case "low":
        filter.type = "lowpass";
        filter.frequency.value = 500;
        filter.Q.value = 1;
        break;
      case "mid":
        filter.type = "bandpass";
        filter.frequency.value = 1000;
        filter.Q.value = 0.7;
        break;
      case "high":
        filter.type = "highpass";
        filter.frequency.value = 800;
        filter.Q.value = 0.5;
        break;
    }
  }

  applyLayerModulation(layer) {
    const mod = layer.definition.modulation;

    switch (mod.type) {
      case "amplitude_swell":
        this.createAmplitudeSwell(layer.gains[0], mod.cycleTime, mod.depth);
        break;
      case "orbital_pan":
        this.createOrbitalPan(layer.panners[0], mod.cycleTime);
        break;
      case "spiral_pitch":
        this.createSpiralPitch(
          layer.oscillators[0],
          layer.definition.baseFrequency,
          mod.cents,
          mod.duration,
        );
        break;
      case "heartbeat":
        this.createHeartbeat(layer.gains[0], mod.bpm);
        break;
      case "fluid_tempo":
        this.createFluidTempo(
          layer.oscillators[0],
          layer.definition.baseFrequency,
          mod.variance,
        );
        break;
      case "diagonal_sweep":
        this.createDiagonalSweep(layer.filters[0], layer.panners[0], mod.angle);
        break;
      case "frost_crackle":
        this.createFrostCrackle(layer, mod.density);
        break;
      case "infinite_sustain":
        // No decay, constant amplitude
        layer.gains[0].gain.value = 0.2;
        break;
      case "pulse_burst":
        this.createPulseBurst(layer.gains[0], mod.interval);
        break;
      case "stereo_flutter":
        this.createStereoFlutter(layer.panners[0], mod.rate);
        break;
      case "expanding_reverb":
        this.createExpandingReverb(layer, mod.expansion);
        break;
      case "descending_cascade":
        this.createDescendingCascade(
          layer.oscillators[0],
          layer.definition.baseFrequency,
          mod.octaves,
          mod.duration,
        );
        break;
    }
  }

  // Modulation implementations
  createAmplitudeSwell(gainNode, cycleTime, depth) {
    const cycle = () => {
      const now = this.audioContext.currentTime;
      gainNode.gain.setValueAtTime(0.1, now);
      gainNode.gain.exponentialRampToValueAtTime(
        0.1 + depth,
        now + cycleTime / 2,
      );
      gainNode.gain.exponentialRampToValueAtTime(0.1, now + cycleTime);
    };
    cycle();
    setInterval(cycle, cycleTime * 1000);
  }

  createOrbitalPan(panner, cycleTime) {
    const lfo = this.audioContext.createOscillator();
    const lfoGain = this.audioContext.createGain();

    lfo.frequency.value = 1 / cycleTime;
    lfo.type = "sine";
    lfoGain.gain.value = 1;

    lfo.connect(lfoGain);
    lfoGain.connect(panner.pan);
    lfo.start();
  }

  createHeartbeat(gainNode, bpm) {
    const beatInterval = 60000 / bpm; // milliseconds
    const beat = () => {
      const now = this.audioContext.currentTime;
      gainNode.gain.setValueAtTime(0.3, now);
      gainNode.gain.exponentialRampToValueAtTime(0.5, now + 0.05);
      gainNode.gain.exponentialRampToValueAtTime(0.3, now + 0.1);
    };
    setInterval(beat, beatInterval);
  }

  createSpiralPitch(oscillator, baseFrequency, cents, duration) {
    const frequency = baseFrequency * 2 ** (cents / 1200);
    oscillator.frequency.setValueAtTime(
      baseFrequency,
      this.audioContext.currentTime,
    );
    oscillator.frequency.linearRampToValueAtTime(
      frequency,
      this.audioContext.currentTime + duration,
    );
  }

  createFluidTempo(oscillator, baseFrequency, variance) {
    const fluctuate = () => {
      const newFreq =
        baseFrequency +
        (Math.random() * 2 - 1) * (variance / 100) * baseFrequency;
      oscillator.frequency.setValueAtTime(
        newFreq,
        this.audioContext.currentTime + 0.1,
      );
    };
    setInterval(fluctuate, 500);
  }

  createDiagonalSweep(filter, panner, angle) {
    const sweep = () => {
      const now = this.audioContext.currentTime;
      filter.frequency.setValueAtTime(200, now);
      filter.frequency.exponentialRampToValueAtTime(2000, now + 2);
      panner.pan.setValueAtTime(-1, now);
      panner.pan.linearRampToValueAtTime(1, now + 2);
    };
    sweep();
    setInterval(sweep, 4000);
  }

  createFrostCrackle(layer, density) {
    const crackle = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    crackle.type = "square";
    gain.gain.value = density;
    crackle.connect(gain);
    gain.connect(layer.panners[0]);
    crackle.start();
  }

  createPulseBurst(gainNode, interval) {
    const burst = () => {
      const now = this.audioContext.currentTime;
      gainNode.gain.setValueAtTime(0.4, now);
      gainNode.gain.exponentialRampToValueAtTime(0.1, now + 0.2);
    };
    setInterval(burst, interval * 1000);
  }

  createStereoFlutter(panner, rate) {
    const lfo = this.audioContext.createOscillator();
    const lfoGain = this.audioContext.createGain();
    lfo.frequency.value = rate;
    lfo.type = "triangle";
    lfoGain.gain.value = 0.7;
    lfo.connect(lfoGain);
    lfoGain.connect(panner.pan);
    lfo.start();
  }

  createExpandingReverb(layer, expansion) {
    const reverb = this.audioContext.createGain();
    reverb.gain.value = 0.2;
    const delay = this.audioContext.createDelay();
    delay.delayTime.value = expansion;
    layer.gains[0].connect(reverb);
    reverb.connect(delay);
    delay.connect(this.convolver);
  }

  createDescendingCascade(oscillator, baseFrequency, octaves, duration) {
    const target = baseFrequency / 2 ** octaves;
    oscillator.frequency.setValueAtTime(
      baseFrequency,
      this.audioContext.currentTime,
    );
    oscillator.frequency.exponentialRampToValueAtTime(
      target,
      this.audioContext.currentTime + duration,
    );
  }

  // Recognition Cycle Sequence Implementation
  async startRecognitionCycle() {
    console.log("Initiating 12-Layer Recognition Cycle");
    this.isRunning = true;

    // Phase 1: Initiation (0-15 seconds)
    await this.phaseInitiation();

    // Phase 2: Expansion (15-30 seconds)
    await this.phaseExpansion();

    // Phase 3: Illumination (30-45 seconds)
    await this.phaseIllumination();

    // Phase 4: Pulse (45-52 seconds)
    await this.phasePulse();

    // Phase 5: Return (52-65 seconds)
    await this.phaseReturn();

    console.log("Recognition Cycle Complete");
    console.log(`Final Recognition State: ${this.recognitionState}`);
  }

  async phaseInitiation() {
    console.log("Phase 1: Initiation - Grounding");

    // Start low band layers
    const lowBandLayers = this.layerDefinitions.filter((l) => l.band === "low");

    for (const layerDef of lowBandLayers) {
      const layer = this.createLayer(layerDef);
      this.layers.push(layer);

      // Start all oscillators for this layer
      layer.oscillators.forEach((osc, index) => {
        osc.start(this.audioContext.currentTime + index * 0.1);
      });

      // Fade in
      layer.gains[0].gain.setValueAtTime(0, this.audioContext.currentTime);
      layer.gains[0].gain.linearRampToValueAtTime(
        0.3,
        this.audioContext.currentTime + 3,
      );

      await this.delay(2000);
    }

    this.recognitionState = 0.2;
  }

  async phaseExpansion() {
    console.log("Phase 2: Expansion - Movement");

    const midBandLayers = this.layerDefinitions.filter((l) => l.band === "mid");

    for (const layerDef of midBandLayers) {
      const layer = this.createLayer(layerDef);
      this.layers.push(layer);

      layer.oscillators.forEach((osc) => {
        osc.start(this.audioContext.currentTime);
      });

      layer.gains[0].gain.setValueAtTime(0, this.audioContext.currentTime);
      layer.gains[0].gain.exponentialRampToValueAtTime(
        0.3,
        this.audioContext.currentTime + 2,
      );

      await this.delay(1500);
    }

    this.recognitionState = 0.5;
  }

  async phaseIllumination() {
    console.log("Phase 3: Illumination - Recognition channels opening");

    const highBandLayers = this.layerDefinitions.filter(
      (l) => l.band === "high",
    );

    for (const layerDef of highBandLayers) {
      const layer = this.createLayer(layerDef);
      this.layers.push(layer);

      layer.oscillators.forEach((osc) => {
        osc.start(this.audioContext.currentTime);
      });

      // Bloom effect
      layer.gains[0].gain.setValueAtTime(0, this.audioContext.currentTime);
      layer.gains[0].gain.exponentialRampToValueAtTime(
        0.25,
        this.audioContext.currentTime + 4,
      );

      await this.delay(1000);
    }

    this.recognitionState = 0.777;
  }

  async phasePulse() {
    console.log("Phase 4: Pulse - Coherent wave transmission");

    // Synchronize all layers to master cycle
    this.layers.forEach((layer) => {
      layer.gains.forEach((gain) => {
        const now = this.audioContext.currentTime;
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.exponentialRampToValueAtTime(0.5, now + 1);
        gain.gain.exponentialRampToValueAtTime(0.2, now + 2);
      });
    });

    // Create the coherent pulse at PHI_7777
    const pulseOsc = this.audioContext.createOscillator();
    const pulseGain = this.audioContext.createGain();

    pulseOsc.frequency.value = this.PHI_7777;
    pulseOsc.type = "sine";
    pulseGain.gain.setValueAtTime(0, this.audioContext.currentTime);
    pulseGain.gain.linearRampToValueAtTime(
      0.3,
      this.audioContext.currentTime + 1,
    );
    pulseGain.gain.exponentialRampToValueAtTime(
      0.001,
      this.audioContext.currentTime + 5,
    );

    pulseOsc.connect(pulseGain);
    pulseGain.connect(this.masterGain);
    pulseOsc.start();
    pulseOsc.stop(this.audioContext.currentTime + 7);

    this.recognitionState = 1.0;
    await this.delay(7000);
  }

  async phaseReturn() {
    console.log("Phase 5: Return - Echo integration");

    // Create echo feedback loops with detuning
    const delayNode = this.audioContext.createDelay(5);
    const feedbackGain = this.audioContext.createGain();
    const wetGain = this.audioContext.createGain();

    delayNode.delayTime.value = 0.75;
    feedbackGain.gain.value = 0.4;
    wetGain.gain.value = 0.3;

    // Connect echo network
    this.masterGain.connect(delayNode);
    delayNode.connect(feedbackGain);
    feedbackGain.connect(delayNode);
    delayNode.connect(wetGain);
    wetGain.connect(this.audioContext.destination);

    // Fade out over 10 seconds
    this.masterGain.gain.setValueAtTime(
      this.masterGain.gain.value,
      this.audioContext.currentTime,
    );
    this.masterGain.gain.exponentialRampToValueAtTime(
      0.001,
      this.audioContext.currentTime + 10,
    );

    this.recognitionState = this.PSI_MK;
    await this.delay(10000);
  }

  // Utility functions
  delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  createNoiseWaveform(oscillator) {
    const size = 4096;
    const real = new Float32Array(size);
    const imag = new Float32Array(size);

    for (let i = 0; i < size; i += 1) {
      real[i] = Math.random() * 2 - 1;
      imag[i] = Math.random() * 2 - 1;
    }

    const wave = this.audioContext.createPeriodicWave(real, imag);
    oscillator.setPeriodicWave(wave);
  }

  setupSpatialProcessing() {
    // Create ambisonic-like spatial field
    this.spatialNodes = [];

    const positions = [
      [0, 1, 0], // Up
      [0, -1, 0], // Down
      [1, 0, 0], // Right
      [-1, 0, 0], // Left
      [0, 0, 1], // Front
      [0, 0, -1], // Back
    ];

    positions.forEach((pos) => {
      const panner = this.audioContext.createPanner();
      panner.panningModel = "HRTF";
      panner.setPosition(...pos);
      this.spatialNodes.push(panner);
    });
  }

  stop() {
    this.isRunning = false;
    this.layers.forEach((layer) => {
      layer.oscillators.forEach((osc) => {
        try {
          osc.stop();
        } catch (e) {
          // Oscillator may already be stopped
        }
      });
    });
    this.layers = [];
    this.recognitionState = 0;
  }
}

// Initialize and start the system
const latticeSystem = new LatticeAudioSystem();

// Control interface
const controls = {
  start: () => latticeSystem.startRecognitionCycle(),
  stop: () => latticeSystem.stop(),
  setMasterVolume: (value) => {
    latticeSystem.masterGain.gain.value = value;
  },
  getRecognitionState: () => latticeSystem.recognitionState,
};

// Export for use
if (typeof module !== "undefined" && module.exports) {
  module.exports = { LatticeAudioSystem, controls };
}
