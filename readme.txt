// size: 12
typedef struct FstorageHeadRegionTag
{
    uint32_t uuid;
    uint8_t model1;
    uint8_t model2; // reserve
    uint16_t ver;
    uint16_t nodeSize;
    uint16_t nodeNum;
} FstorageHeadRegion;

                model1  model2
运动统计数据:      S
运动计圈数据:      K
运动实时数据:      R
血氧数据:          B        O
心率数据:          H        R
睡眠数据:          N        P
计步数据:          F        S
血压数据:          B        P

uuid:时间（天），运动记录
ver:对应数据解析版本
nodeSize:对应子数据大小
nodeNum:对应子数据数量


// size: 92
typedef struct _StoreStatisticData
{
    uint8_t mode;
    uint8_t averageHr;
    uint8_t maxHr;
    int8_t timezone;                    // [-11, 12]
    uint16_t distributed[5];
    uint16_t maxCadence;                // unit: per min
    uint32_t riseAltitude;              // unit: m
    uint32_t dropAltitude;              // unit: m
    uint32_t maxAltitude;               // unit: m
    uint32_t minAltitude;               // unit: m
    int32_t altitude;                   // unit: m
    uint32_t calorie;
    uint32_t bestPace;                  // unit: sec per kilometer / meter per hour
    uint32_t timestamp;
    uint32_t accomplishTime;            // unit: sec
    uint32_t pauseTime;                 // unit: sec
    uint32_t distance;                  // unit: meter
    uint32_t calibrateDistance;         // unit: meter
    uint32_t step;
    uint32_t oLongtitude;               // originate
    uint32_t oLatitude;
    uint32_t tLongtitude;               // terminate
    uint32_t tLatitude;
    uint8_t oLongitude_ew;
    uint8_t oLatitude_ns;
    uint8_t tLongitude_ew;
    uint8_t tLatitude_ns;
    uint8_t unitType;                   // bit0~7: 0 ~ 1 0:Centigrade, 1:Fahrenheit; 2 ~ 3 0:meter 1:mile 2:yard 3:foot
    uint8_t weatherCondition;
    int16_t temperature;
} StoreStatisticsData;

// size: 24
typedef struct _StoreRealtimeData
{
    uint8_t pause;
    uint8_t hr; // reserve
    uint8_t longitude_ew;
    uint8_t latitude_ns;
    uint16_t cadence;
    int16_t temperature;
    uint32_t pace;
    uint32_t latitude;
    uint32_t longitude;
    int8_t deltaAltitude;
    uint8_t deltaDistance;
    uint16_t reserve;
} StoreRealtimeData;

// size: 28
typedef struct _StoreCircleElement
{
    uint32_t pace;
    uint32_t elapseTime;
    uint32_t pauseTime;
    uint32_t unit;
    uint32_t longtitude;
    uint32_t latitude;
    uint8_t longitude_ew;
    uint8_t latitude_ns;
    uint16_t reverse;
} StoreCircleElement;

// size: 4
typedef struct _StepHourInfo
{
    uint16_t step;
    uint16_t distance;          // unit: m
} StepHourInfo;

// size: 112
typedef struct _StepDetailInfo
{
    uint32_t timestamp;
    int8_t timezone;            // [-11, 12], only be modified when date change
    uint8_t sedentaryCount;     // sedentary count in one day
    uint16_t reverse;           // reserve
    uint32_t calorieBmr;        // unit: c, from 00:00 to this hour, or this minute, this second
    uint32_t calorieSport;      // unit: c, consumption of a sport in this day
    StepHourInfo info[24];
} StepDetailInfo;