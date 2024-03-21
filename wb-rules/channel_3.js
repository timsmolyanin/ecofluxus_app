defineVirtualDevice('Channel_3', {
  title: 'Channel_3',
  cells: {
  ControlMode: {
      type: 'text',
      title: 'ControlMode',
      value: '',
      order: 1,
      readonly: false
    },
  RoomName: {
      type: 'text',
      title: 'RoomName',
      value: '',
      order: 1,
      readonly: false
    },
  RoomType: {
      type: 'text',
      title: 'RoomType',
      value: '',
      order: 1,
      readonly: false
    },
  VentPipeLength: {
      type: 'value',
      title: 'VentPipeLength',
      value: '0',
      order: 1,
      readonly: false
    },
  VentPipeIOHeight: {
      type: 'value',
      title: 'VentPipeIOHeight',
      value: '0',
      order: 1,
      readonly: false
    },
  VentPipeDiameter: {
      type: 'value',
      title: 'VentPipeDiameter',
      value: '0',
      order: 1,
      readonly: false
    },
  RoomArea: {
      type: 'value',
      title: 'RoomArea',
      value: '0',
      order: 1,
      readonly: false
    },
  AirExchangeSet: {
      type: 'value',
      title: 'AirExchangeSet',
      value: '0',
      order: 1,
      readonly: false
    },
  AirExchangeCalc: {
      type: 'value',
      title: 'AirExchangeCalc',
      value: '0',
      order: 1,
      readonly: false
    },
  EcoCoefState: {
      type: 'value',
      title: 'EcoCoefState',
      value: '0',
      order: 1,
      readonly: false
    },
  EcoCoefValue: {
      type: 'value',
      title: 'EcoCoefValue',
      value: '0',
      order: 1,
      readonly: false
    },
  EcoCO2State: {
      type: 'value',
      title: 'EcoCO2State',
      value: '0',
      order: 1,
      readonly: false
    },
  EcoCO2State: {
      type: 'value',
      title: 'EcoCO2State',
      value: '0',
      order: 1,
      readonly: false
    },
  WeekStart: {
      type: 'value',
      title: 'WeekStart',
      value: '0',
      order: 1,
      readonly: false
    },
  WeekStop: {
      type: 'value',
      title: 'WeekStop',
      value: '0',
      order: 1,
      readonly: false
    },
  WeekendStart: {
      type: 'value',
      title: 'WeekendStart',
      value: '0',
      order: 1,
      readonly: false
    },
  WeekendStop: {
      type: 'value',
      title: 'WeekendStop',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod1State: {
      type: 'value',
      title: 'SWPeriod1State',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod1Start: {
      type: 'value',
      title: 'SWPeriod1Start',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod1Stop: {
      type: 'value',
      title: 'SWPeriod1Stop',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod2State: {
      type: 'value',
      title: 'SWPeriod2State',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod2Start: {
      type: 'value',
      title: 'SWPeriod2Start',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod2Stop: {
      type: 'value',
      title: 'SWPeriod2Stop',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod3State: {
      type: 'value',
      title: 'SWPeriod3State',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod3Start: {
      type: 'value',
      title: 'SWPeriod3Start',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod3Stop: {
      type: 'value',
      title: 'SWPeriod3Stop',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod4State: {
      type: 'value',
      title: 'SWPeriod4State',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod4Start: {
      type: 'value',
      title: 'SWPeriod4Start',
      value: '0',
      order: 1,
      readonly: false
    },
  SWPeriod4Stop: {
      type: 'value',
      title: 'SWPeriod4Stop',
      value: '0',
      order: 1,
      readonly: false
    },
  SetAngle: {
      type: 'value',
      title: 'SetAngle',
      value: '0',
      order: 1,
      readonly: false
    },
  FeedbackAngle: {
      type: 'value',
      title: 'FeedbackAngle',
      value: '0',
      order: 1,
      readonly: true
    },
  LastSetAngle: {
      type: 'value',
      title: 'LastSetAngle',
      value: '0',
      order: 1,
      readonly: false
    },
  SetLastAngle: {
      type: 'value',
      title: 'SetLastAngle',
      value: '0',
      order: 1,
      readonly: false
    },
  UpdatePeriod: {
      type: 'value',
      title: 'UpdatePeriod',
      value: '0',
      order: 1,
      readonly: false
    },
  VentWidState: {
      type: 'text',
      title: 'VentWidState',
      value: '',
      order: 1,
      readonly: false
  }
  }
});

// from 0-90 degree to voltage
var sk = 1.11111111111;
var gk = 8.89503;

defineRule("ch3_from_angle_to_voltage", {
whenChanged: "Channel_3/SetAngle",
then: function(newValue, devName, cellName) {
  dev["wb-mao4_26/Channel 3 Dimming Level"] = sk * newValue;
}
});

// from voltage to angle
defineRule("ch3_from_voltage_to_angle", {
whenChanged: "wb-mai6_89/IN 2 N Voltage",
then: function(newValue, devName, cellName) {
  angle_val = Math.round(gk * newValue)+1;
  if (angle_val > 90){
    dev["Channel_3/FeedbackAngle"] = 90;
  }
  else if (angle_val <= 1){
    dev["Channel_3/FeedbackAngle"] = 0;
  }
  else{
    dev["Channel_3/FeedbackAngle"] = angle_val;
  }
}
});

var last_set_angle = 0;

defineRule("last_set_angle", {
whenChanged: "Channel_3/LastSetAngle",
then: function(newValue, devName, cellName) {
  last_set_angle = newValue;
}
});

defineRule("set_last_angle", {
whenChanged: "Channel_3/SetLastAngle",
then: function(newValue, devName, cellName) {
  dev["Channel_3/SetAngle"] = last_set_angle;
}
});
