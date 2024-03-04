defineVirtualDevice('Channel_2', {
  title: 'Channel_2',
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
  AirExchangeValue: {
      type: 'value',
      title: 'AirExchangeValue',
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
  }
}
});
var sk = 10 / 9;
var gk = 0.009;

// from 0-90 degree to voltage
defineRule("ch2_from_angle_to_voltage", {
whenChanged: "Channel_2/SetAngle",
then: function(newValue, devName, cellName) {
  dev["wb-mao4_26/Channel 2 Dimming Level"] = sk * newValue;
}
});

// from voltage to angle
defineRule("ch2_from_voltage_to_angle", {
whenChanged: "wb-mai6_89/IN 2 N Value",
then: function(newValue, devName, cellName) {
  dev["Channel_2/FeedbackAngle"] = Math.floor(gk * newValue);
}
});