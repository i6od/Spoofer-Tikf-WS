import asyncio
import websockets
import json
import logging
from typing import Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JSON events to rotate through
EVENTS = [
    {
        "event": "subscribe",
        "data": {
            "exhibitionType": 2,
            "subMonth": 1,
            "subscribingStatus": 1,
            "userId": "7363068828409086994",
            "secUid": "MS4wLjABAAAAZgEvGdGJo0nuB8nUkuvixS_hZCqwe-sU0WUHslwMCUNS_nLEH6HCCLvf_CbI7kD-",
            "uniqueId": "l..priv08",
            "nickname": "Lil",
            "profilePictureUrl": "https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/be67d45946d91c41a1e0b2aecdb4efee.webp?lk3s=a5d48078&nonce=76415&refresh_token=7c0a3b04301ee6970b90693cfb672b49&x-expires=1739628000&x-signature=SRfRsSjzUd7SxePyiYrAmDDM3LA%3D&shp=a5d48078&shcp=fdd36af4",
            "followRole": 0,
            "userBadges": [],
            "userSceneTypes": [],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/be67d45946d91c41a1e0b2aecdb4efee.webp?lk3s=a5d48078&nonce=76415&refresh_token=7c0a3b04301ee6970b90693cfb672b49&x-expires=1739628000&x-signature=SRfRsSjzUd7SxePyiYrAmDDM3LA%3D&shp=a5d48078&shcp=fdd36af4",
                    "https://p16-sign-sg.tiktokcdn.com/aweme/100x100/tos-alisg-avt-0068/be67d45946d91c41a1e0b2aecdb4efee.jpeg?lk3s=a5d48078&nonce=41759&refresh_token=28f3ba30209e58b5c0c14e623514ea74&x-expires=1739628000&x-signature=haIMJkrnBce5X8W9xHp5akbnXsQ%3D&shp=a5d48078&shcp=fdd36af4"
                ]
            },
            "followInfo": {
                "followingCount": 79,
                "followerCount": 12,
                "followStatus": 0,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": False,
            "topGifterRank": 0,
            "gifterLevel": 0,
            "teamMemberLevel": 0,
            "msgId": "7470903979216472874",
            "createTime": "1739456054393",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "xuhsy"
        }
    },
    {
        "event": "gift",
        "data": {
            "giftId": 5655,
            "repeatCount": 2,
            "groupId": "1741369871051",
            "userId": "6902109974527017990",
            "secUid": "MS4wLjABAAAAmF7E3DLNtHQSbf5zd7kQd1onfbIHDIVs3WfJIs3hcvUInkVNMtqgP3op4RILRKBc",
            "uniqueId": "brianiac5.1",
            "nickname": "Brian 5.1 🐾",
            "profilePictureUrl": "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=aa19d004&x-expires=1741539600&x-signature=WJKBkpd2Yvl5nxC2mxbTBpJ6T7w%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
            "followRole": 3,
            "userBadges": [
                {
                    "type": "image",
                    "badgeSceneType": 4,
                    "displayType": 1,
                    "url": "https://p19-webcast.tiktokcdn.com/webcast-sg/sub_4b9515c5f41ab2e85e8afafbdc2ccb452cffeb06aa0e16916448be5fc4e1445e~tplv-obj.image"
                },
                {
                    "type": "privilege",
                    "privilegeId": "7341746249734966036",
                    "level": 2,
                    "badgeSceneType": 4
                },
                {
                    "type": "privilege",
                    "privilegeId": "7138381747292591908",
                    "level": 18,
                    "badgeSceneType": 8
                },
                {
                    "type": "privilege",
                    "privilegeId": "7341746249734966036",
                    "level": 2,
                    "badgeSceneType": 4
                },
                {
                    "type": "privilege",
                    "privilegeId": "7196929090442545925",
                    "level": 28,
                    "badgeSceneType": 10
                }
            ],
            "userSceneTypes": [4, 8, 4, 10],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=aa19d004&x-expires=1741539600&x-signature=WJKBkpd2Yvl5nxC2mxbTBpJ6T7w%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
                    "https://p16-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=70da347a&x-expires=1741539600&x-signature=PJTGikDmtp9LDtFfjQ5dDvy3pSE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
                    "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.jpeg?dr=9640&refresh_token=a56545b1&x-expires=1741539600&x-signature=WUCuhFLSZidhLLxfj1ULrTiZ9f8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5"
                ]
            },
            "followInfo": {
                "followingCount": 478,
                "followerCount": 1036,
                "followStatus": 3,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": True,
            "topGifterRank": 0,
            "gifterLevel": 18,
            "teamMemberLevel": 28,
            "msgId": "7479126550374271790",
            "createTime": "1741369872746",
            "displayType": "webcast_aweme_gift_send_messageNew",
            "label": "{0:user} sent {1:gift} × {2:string}",
            "repeatEnd": False,
            "gift": {
                "gift_id": 5655,
                "repeat_count": 2,
                "repeat_end": 0,
                "gift_type": 1
            },
            "describe": "sent Rose",
            "giftType": 1,
            "diamondCount": 1,
            "giftName": "Rose",
            "giftPictureUrl": "https://p19-webcast.tiktokcdn.com/img/maliva/webcast-va/eba3a9bb85c33e017f3648eaf88d7189~tplv-obj.png",
            "timestamp": 1741369872749,
            "receiverUserId": "6811664027753268225",
            "originalName": "Rose",
            "originalDescribe": "Sent Rose",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "white_spa_cher"
        }
    },
    {
        "event": "follow",
        "data": {
            "userId": "6833839589649662982",
            "secUid": "MS4wLjABAAAANKCsuz8S6eSwG5CV4cwkhTl3SOgq9xlKXs2cwuipKLyPxPhIW3EfDTZSLFIh9cPk",
            "uniqueId": "_am_eliesr",
            "nickname": "amelie",
            "profilePictureUrl": "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.webp?dr=10399&refresh_token=a6b2f648&x-expires=1741539600&x-signature=W6LHH%2BcSYucdPWMzg4C5kyO1KOA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a",
            "followRole": 1,
            "userBadges": [],
            "userSceneTypes": [],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.webp?dr=10399&refresh_token=a6b2f648&x-expires=1741539600&x-signature=W6LHH%2BcSYucdPWMzg4C5kyO1KOA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a",
                    "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.jpeg?dr=10399&refresh_token=e7e7bcdf&x-expires=1741539600&x-signature=tgP6UTUlgP42Q3FFk%2FFzZvOwx7s%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a"
                ]
            },
            "followInfo": {
                "followingCount": 3442,
                "followerCount": 35,
                "followStatus": 1,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": False,
            "topGifterRank": 0,
            "gifterLevel": 0,
            "teamMemberLevel": 0,
            "createTime": "1741369800451",
            "msgId": "7479126330336987926",
            "displayType": "pm_main_follow_message_viewer_2",
            "label": "{0:user} followed the LIVE creator",
            "profile": "_am_eliesr",
            "name": "_am_eliesr",
            "username": "_am_eliesr",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "white_spa_cher"
        }
    },
    {
        "event": "gift",
        "data": {
            "giftId": 5655,
            "repeatCount": 2,
            "groupId": "1741369871051",
            "userId": "6902109974527017990",
            "secUid": "MS4wLjABAAAAmF7E3DLNtHQSbf5zd7kQd1onfbIHDIVs3WfJIs3hcvUInkVNMtqgP3op4RILRKBc",
            "uniqueId": "brianiac5.1",
            "nickname": "Brian 5.1 🐾",
            "profilePictureUrl": "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=aa19d004&x-expires=1741539600&x-signature=WJKBkpd2Yvl5nxC2mxbTBpJ6T7w%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
            "followRole": 3,
            "userBadges": [
                {
                    "type": "image",
                    "badgeSceneType": 4,
                    "displayType": 1,
                    "url": "https://p19-webcast.tiktokcdn.com/webcast-sg/sub_4b9515c5f41ab2e85e8afafbdc2ccb452cffeb06aa0e16916448be5fc4e1445e~tplv-obj.image"
                },
                {
                    "type": "privilege",
                    "privilegeId": "7341746249734966036",
                    "level": 2,
                    "badgeSceneType": 4
                },
                {
                    "type": "privilege",
                    "privilegeId": "7138381747292591908",
                    "level": 18,
                    "badgeSceneType": 8
                },
                {
                    "type": "privilege",
                    "privilegeId": "7341746249734966036",
                    "level": 2,
                    "badgeSceneType": 4
                },
                {
                    "type": "privilege",
                    "privilegeId": "7196929090442545925",
                    "level": 28,
                    "badgeSceneType": 10
                }
            ],
            "userSceneTypes": [4, 8, 4, 10],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=aa19d004&x-expires=1741539600&x-signature=WJKBkpd2Yvl5nxC2mxbTBpJ6T7w%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
                    "https://p16-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.webp?dr=9640&refresh_token=70da347a&x-expires=1741539600&x-signature=PJTGikDmtp9LDtFfjQ5dDvy3pSE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5",
                    "https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-avt-0068-tx/7310052407235313707~tplv-tiktokx-cropcenter:100:100.jpeg?dr=9640&refresh_token=a56545b1&x-expires=1741539600&x-signature=WUCuhFLSZidhLLxfj1ULrTiZ9f8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=useast5"
                ]
            },
            "followInfo": {
                "followingCount": 478,
                "followerCount": 1036,
                "followStatus": 3,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": True,
            "topGifterRank": 0,
            "gifterLevel": 18,
            "teamMemberLevel": 28,
            "msgId": "7479126550374271790",
            "createTime": "1741369872746",
            "displayType": "webcast_aweme_gift_send_messageNew",
            "label": "{0:user} sent {1:gift} × {2:string}",
            "repeatEnd": False,
            "gift": {
                "gift_id": 5655,
                "repeat_count": 2,
                "repeat_end": 0,
                "gift_type": 1
            },
            "describe": "sent Heart Me",
            "giftType": 1,
            "diamondCount": 1,
            "giftName": "Heart Me",
            "giftPictureUrl": "https://p19-webcast.tiktokcdn.com/img/maliva/webcast-va/eba3a9bb85c33e017f3648eaf88d7189~tplv-obj.png",
            "timestamp": 1741369872749,
            "receiverUserId": "6811664027753268225",
            "originalName": "Heart Me",
            "originalDescribe": "Sent Heart Me",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "white_spa_cher"
        }
    },
    {
        "event": "follow",
        "data": {
            "userId": "6833839589649662982",
            "secUid": "MS4wLjABAAAANKCsuz8S6eSwG5CV4cwkhTl3SOgq9xlKXs2cwuipKLyPxPhIW3EfDTZSLFIh9cPk",
            "uniqueId": "_am_eliesr",
            "nickname": "amelie",
            "profilePictureUrl": "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.webp?dr=10399&refresh_token=a6b2f648&x-expires=1741539600&x-signature=W6LHH%2BcSYucdPWMzg4C5kyO1KOA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a",
            "followRole": 1,
            "userBadges": [],
            "userSceneTypes": [],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.webp?dr=10399&refresh_token=a6b2f648&x-expires=1741539600&x-signature=W6LHH%2BcSYucdPWMzg4C5kyO1KOA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a",
                    "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-euttp/de9d5aef0b08ebaa70f408602871739b~tplv-tiktokx-cropcenter:100:100.jpeg?dr=10399&refresh_token=e7e7bcdf&x-expires=1741539600&x-signature=tgP6UTUlgP42Q3FFk%2FFzZvOwx7s%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=no1a"
                ]
            },
            "followInfo": {
                "followingCount": 3442,
                "followerCount": 35,
                "followStatus": 1,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": False,
            "topGifterRank": 0,
            "gifterLevel": 0,
            "teamMemberLevel": 0,
            "createTime": "1741369800451",
            "msgId": "7479126330336987926",
            "displayType": "pm_main_follow_message_viewer_2",
            "label": "{0:user} followed the LIVE creator",
            "profile": "_am_eliesr",
            "name": "_am_eliesr",
            "username": "_am_eliesr",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "white_spa_cher"
        }
    },
    {
        "event": "like",
        "data": {
            "likeCount": 15,
            "totalLikeCount": 687421,
            "userId": "7156645093553931270",
            "secUid": "MS4wLjABAAAA1R9Vf8s47_BHJl-LFrWwT3uRGVdofAFAyRVaklaxhw0DYbEbRz6Lez595NjwEGdK",
            "uniqueId": "h4ma5.11",
            "nickname": "ᴛᴏᴘ ᴏɴᴇ ✪",
            "profilePictureUrl": "https://p77-sign-sg.tiktokcdn.com/tos-alisg-avt-0068/2ffc736d2e0f4230d0e216a41e19966d~tplv-tiktokx-cropcenter:100:100.webp?dr=14579&refresh_token=d01c6125&x-expires=1742245200&x-signature=F7uYvQ2emR6j0gTPEP7fej9iqhU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my",
            "followRole": 1,
            "userBadges": [
                {
                    "type": "privilege",
                    "privilegeId": "7196929090442513157",
                    "level": 9,
                    "badgeSceneType": 10
                }
            ],
            "userSceneTypes": [10],
            "userDetails": {
                "createTime": "0",
                "bioDescription": "",
                "profilePictureUrls": [
                    "https://p77-sign-sg.tiktokcdn.com/tos-alisg-avt-0068/2ffc736d2e0f4230d0e216a41e19966d~tplv-tiktokx-cropcenter:100:100.webp?dr=14579&refresh_token=d01c6125&x-expires=1742245200&x-signature=F7uYvQ2emR6j0gTPEP7fej9iqhU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my",
                    "https://p16-sign-sg.tiktokcdn.com/tos-alisg-avt-0068/2ffc736d2e0f4230d0e216a41e19966d~tplv-tiktokx-cropcenter:100:100.webp?dr=14579&refresh_token=bcb3b310&x-expires=1742245200&x-signature=7TMh8Lhh1PGdD8p4IX1MU6JvEqo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my",
                    "https://p77-sign-sg.tiktokcdn.com/tos-alisg-avt-0068/2ffc736d2e0f4230d0e216a41e19966d~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6df62bbc&x-expires=1742245200&x-signature=OStnMvtL7wTux3B6bRsYcIvBkPE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my"
                ]
            },
            "followInfo": {
                "followingCount": 322,
                "followerCount": 344,
                "followStatus": 1,
                "pushStatus": 0
            },
            "isModerator": False,
            "isNewGifter": False,
            "isSubscriber": False,
            "topGifterRank": 0,
            "gifterLevel": 0,
            "teamMemberLevel": 9,
            "msgId": "7482149051539292424",
            "createTime": "1742073580115",
            "displayType": "pm_mt_msg_viewer",
            "label": "{0:user} liked the LIVE",
            "tikfinityUserId": 1083548,
            "tikfinityUsername": "speed0.11"
        }
    }
]

# Global variables
connected_clients: Set[websockets.WebSocketServerProtocol] = set()
current_event_index = 0

async def handle_client(websocket):
    """Handle new client connections"""
    connected_clients.add(websocket)
    logger.info(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        # Keep the connection alive and handle any incoming messages
        async for message in websocket:
            logger.info(f"Received message from client: {message}")
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    finally:
        connected_clients.remove(websocket)
        logger.info(f"Client removed. Total clients: {len(connected_clients)}")

async def broadcast_events():
    """Broadcast events to all connected clients in rotation"""
    global current_event_index
    
    while True:
        if connected_clients:
            # Get current event
            event = EVENTS[current_event_index]
            event_json = json.dumps(event)
            
            # Send to all connected clients
            disconnected_clients = []
            for client in connected_clients:
                try:
                    await client.send(event_json)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client)
            
            # Remove disconnected clients
            for client in disconnected_clients:
                connected_clients.discard(client)
            
            if connected_clients:
                logger.info(f"Sent {event['event']} event to {len(connected_clients)} clients")
            
            # Move to next event (rotate)
            current_event_index = (current_event_index + 1) % len(EVENTS)
        
        # Wait 3 seconds before sending next event
        await asyncio.sleep(3)

async def main():
    """Main server function"""
    host = "localhost"
    port = 21213
    
    logger.info(f"Starting WebSocket server on ws://{host}:{port}")
    
    # Start the WebSocket server
    server = websockets.serve(handle_client, host, port)
    
    # Start the event broadcasting task
    broadcast_task = asyncio.create_task(broadcast_events())
    
    # Run both tasks concurrently
    await asyncio.gather(
        server,
        broadcast_task
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
