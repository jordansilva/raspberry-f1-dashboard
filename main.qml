import QtQuick 2.9
import QtQuick.Window 2.9
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.2
import QtQuick.Extras 1.4

ApplicationWindow {
    id: window
    title: qsTr("Hello World")
    width: 800
    height: 480
    color: "#000000"
    visible: true
    Component.onCompleted: {
//        window.showFullScreen()
    }



    Rectangle {
        id: rectangle1
        width: 800
        height: 480
        color: "#000000"

        FontLoader {
            id: fontDigital7
            source: "fonts/digital-7.ttf"
        }

        FontLoader {
            id: fontDefault
            source: "fonts/BebasNeue-Regular.ttf"
        }

        Text {
            id: txtGear
            objectName: "txtGear"
            x: 0
            y: 80
            width: 150
            height: 200
            color: "#ffffff"
            text: car.gear
            font.family: fontDigital7.name
            anchors.horizontalCenter: parent.horizontalCenter
            font.capitalization: Font.AllUppercase
            horizontalAlignment: Text.AlignHCenter
            font.bold: true
            font.pixelSize: 250

            Label {
                id: txtDiffPreviousLap
                objectName: "txtDiffPreviousLap"
                x: 2
                width: 150
                height: 34
                color: "#28f054"
                text: lap.diffPreviousLap
                visible: !carStatus.pitLimiterStatus
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                font.weight: Font.DemiBold
                font.family: fontDefault.name
                anchors.top: parent.bottom
                anchors.topMargin: 10
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.rightMargin: 10
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtPitLimiter
                objectName: "txtPitLimiter"
                x: 2
                color: "#ffffff"
                text: "Pit Limiter"
                visible: carStatus.pitLimiterStatus
                verticalAlignment: Text.AlignVCenter
                font.family: fontDefault.name
                font.letterSpacing: 2
                font.wordSpacing: 5
                anchors.top: parent.bottom
                anchors.topMargin: 10
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.rightMargin: 10
                font.pixelSize: 46
                font.bold: true

                Rectangle {
                    width: 20
                    height: 20
                    color: "#FF3431"
                    anchors.right: parent.left
                    anchors.rightMargin: 10
                    anchors.verticalCenter: parent.verticalCenter
                }

                Rectangle {
                    width: 20
                    height: 20
                    color: "#FF3431"
                    anchors.left: parent.right
                    anchors.leftMargin: 10
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }

        Rectangle {
            id: info1
            x: 0
            y: 100
            width: 250
            height: 142
            color: "#000000"
            anchors.left: parent.left
            anchors.leftMargin: 20
            border.width: 2
            border.color: "gray"

            Rectangle {
                width: 250
                height: 48
                color: "#808080"
                Label {
                    id: txtSpeed
                    objectName: "txtSpeed"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                    text: car.speed + " KPM"
                    fontSizeMode: Text.HorizontalFit
                    font.pixelSize: 36
                    font.styleName: "Bold"
                    font.bold: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            Label {
                id: txtLap
                objectName: "txtLap"
                y: 57
                width: 74
                height: 36
                color: "#ffffff"
                text: "L" + lap.currentLapNum
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pixelSize: 30
                font.bold: true
            }


            Label {
                id: txtPosition
                objectName: "txtPosition"
                x: 176
                y: 57
                width: 66
                height: 36
                color: "#ffffff"
                text: "P" + lap.position
                horizontalAlignment: Text.AlignRight
                anchors.right: parent.right
                anchors.rightMargin: 10
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtCarAhead
                objectName: "txtCarAhead"
                x: 8
                y: 99
                width: 76
                height: 36
                color: "#ffffff"
                text: qsTr("3.4")
                anchors.leftMargin: 10
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtCarBehind
                objectName: "txtCarBehind"
                x: 96
                y: 99
                color: "#28f054"
                text: carStatus.fuelRemainingLaps
                anchors.right: parent.right
                anchors.rightMargin: 10
                horizontalAlignment: Text.AlignRight
                font.pixelSize: 30
                font.bold: true
            }
        }

        Rectangle {
            id: info2
            x: 0
            y: 100
            width: 250
            height: 142
            color: "#000000"
            anchors.right: parent.right
            anchors.rightMargin: 20
            border.width: 2

            Rectangle {
                width: 250
                height: 48
                color: "#808080"
                Label {
                    id: txtLapTime
                    objectName: "txtLapTime"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    color: "#ffffff"
                    text: lap.currentLapTime
                    fontSizeMode: Text.HorizontalFit
                    font.pixelSize: 36
                    font.styleName: "Bold"
                    font.bold: true
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
            Label {
                id: txtTireLeft1
                objectName: "txtTireLeft1"
                y: 57
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresInnerTemperature[2] + "°C"
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtTireLeft2
                objectName: "txtTireLeft2"
                y: 99
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresInnerTemperature[0] + "°C"
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtTireRight1
                objectName: "txtTireRight1"
                x: 145
                y: 57
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresInnerTemperature[3] + "°C"
                horizontalAlignment: Text.AlignRight
                anchors.rightMargin: 10
                anchors.right: parent.right
                font.pixelSize: 30
                font.bold: true
            }

            Label {
                id: txtTireRight2
                objectName: "txtTireRight2"
                x: 143
                y: 99
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresInnerTemperature[1] + "°C"
                anchors.right: parent.right
                anchors.rightMargin: 10
                horizontalAlignment: Text.AlignRight
                font.pixelSize: 30
                font.bold: true
            }
            border.color: "#808080"
        }

        Rectangle {
            property int percentage: carStatus.ersStoreEnergy
            id: progressEnergyERS
            width: 600
            height: 30
            radius: height / 2
            color: "transparent"
            border.color: "yellow"
            border.width: 1
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 100

            Item {
                id: progressEnergyERSItem
                anchors.bottom: parent.bottom
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width * parent.percentage / 100
                clip: true

                Rectangle {
                    width: progressEnergyERS.width
                    height: progressEnergyERS.height
                    radius: height / 2
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    color: "yellow"
                }
            }


            Label {
                id: txtLevelERS
                objectName: "txtLevelERS"
                x: -29
                y: 0
                width: 19
                height: 34
                color: "#ffff00"
                text: carStatus.ersDeployMode
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.left
                anchors.rightMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignRight
                font.family: fontDefault.name
                font.pixelSize: 32
                font.weight: Font.DemiBold
                font.bold: true

                Image {
                    id: image
                    x: 0
                    y: 0
                    width: 28
                    height: 28
                    sourceSize.height: 30
                    sourceSize.width: 30
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.left
                    anchors.rightMargin: 0
                    fillMode: Image.PreserveAspectFit
                    source: "images/lightning-outline-filled.png"
                }
            }

            Label {
                id: txtPercentageERS
                objectName: "txtPercentageERS"
                y: 0
                width: 66
                height: 34
                color: "yellow"
                text: carStatus.ersStoreEnergyPercentage + "%"
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.right
                anchors.leftMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignLeft
                font.family: fontDefault.name
                anchors.rightMargin: 10
                font.pixelSize: 32
                font.weight: Font.DemiBold
                font.bold: true
            }
        }

        //D Progress
        Rectangle {
            property int percentage: carStatus.ersDeployedThisLap
            id: progressD
            width: 250
            height: 30
            radius: height / 2
            color: "transparent"
            border.color: "#ffffff"
            border.width: 1
            anchors.left: parent.left
            anchors.leftMargin: 100
            anchors.bottomMargin: 40
            anchors.bottom: parent.bottom

            Item {
                id: txtProgressDRect
                anchors.bottom: parent.bottom
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width * parent.percentage / 100
                clip: true

                Rectangle {
                    width: progressD.width
                    height: progressD.height
                    radius: height / 2
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    color: "#ffffff"
                }
            }

            Label {
                id: txtD
                x: -29
                y: 0
                width: 19
                height: 34
                color: "#ffffff"
                text: qsTr("D")
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignRight
                font.family: fontDefault.name
                anchors.rightMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.left
                font.pixelSize: 32
                font.weight: Font.DemiBold
                font.bold: true
            }
        }

        Rectangle {
            property int percentage: carStatus.ersHarvestedThisLap
            id: progressH
            width: 250
            height: 30
            radius: height / 2
            color: "transparent"
            border.color: "#ffffff"
            border.width: 1
            anchors.right: parent.right
            anchors.rightMargin: 100
            anchors.bottomMargin: 40
            anchors.bottom: parent.bottom

            Item {
                id: cliprect
                anchors.bottom: parent.bottom
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width * parent.percentage / 100
                clip: true

                Rectangle {
                    width: progressH.width
                    height: progressH.height
                    radius: height / 2
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    color: "#ffffff"
                }
            }

            Label {
                id: txtH
                y: 0
                width: 19
                height: 34
                color: "#ffffff"
                text: qsTr("H")
                anchors.left: parent.right
                anchors.leftMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignLeft
                font.family: fontDefault.name
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 32
                font.weight: Font.DemiBold
                font.bold: true
                renderType: Text.NativeRendering
            }
        }

        RowLayout {
            id: rectangle
            x: 20
            y: 20
            width: 735
            height: 44
            anchors.horizontalCenter: parent.horizontalCenter

            Rectangle {
                id: led0
                x: 707
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[0]
                    anchors.centerIn: parent
                    color: "#6FD269"
                }
            }

            Rectangle {
                id: led1
                x: 442
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[1]
                    anchors.centerIn: parent
                    color: "#6FD269"
                }
            }

            Rectangle {
                id: led2
                x: 408
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[2]
                    anchors.centerIn: parent
                    color: "#6FD269"
                }
            }

            Rectangle {
                id: led3
                x: 374
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[3]
                    anchors.centerIn: parent
                    color: "#6FD269"
                }
            }

            Rectangle {
                id: led4
                x: 340
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[4]
                    anchors.centerIn: parent
                    color: "#6FD269"
                }
            }

            Rectangle {
                id: led5
                x: 306
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[5]
                    anchors.centerIn: parent
                    color: "#DE0C10"
                }
            }

            Rectangle {
                id: led6
                x: 272
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[6]
                    anchors.centerIn: parent
                    color: "#DE0C10"
                }
            }

            Rectangle {
                id: led7
                x: 238
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[7]
                    anchors.centerIn: parent
                    color: "#DE0C10"
                }
            }

            Rectangle {
                id: led8
                x: 204
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[8]
                    anchors.centerIn: parent
                    color: "#DE0C10"
                }
            }

            Rectangle {
                id: led9
                x: 170
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[9]
                    anchors.centerIn: parent
                    color: "#DE0C10"
                }
            }

            Rectangle {
                id: led10
                x: 136
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[10]
                    anchors.centerIn: parent
                    color: "#0F7BD7"
                }
            }

            Rectangle {
                id: led11
                x: 102
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[11]
                    anchors.centerIn: parent
                    color: "#0F7BD7"
                }
            }

            Rectangle {
                id: led12
                x: 68
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[12]
                    anchors.centerIn: parent
                    color: "#0F7BD7"
                }
            }

            Rectangle {
                id: led13
                x: 34
                y: 0
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[13]
                    anchors.centerIn: parent
                    color: "#0F7BD7"
                }
            }

            Rectangle {
                id: led14
                width: 28
                height: 28
                color: "transparent"
                anchors.verticalCenter: parent.verticalCenter

                StatusIndicator {
                    active: revLights[14]
                    anchors.centerIn: parent
                    color: "#0F7BD7"
                }
            }

        }
    }



}

/*##^##
Designer {
    D{i:7;anchors_y:57}
}
##^##*/
