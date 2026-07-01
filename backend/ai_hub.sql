/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80030
Source Host           : localhost:3306
Source Database       : ai_hub

Target Server Type    : MYSQL
Target Server Version : 80030
File Encoding         : 65001

Date: 2026-07-01 15:29:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`),
  KEY `ix_message_id` (`id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of message
-- ----------------------------
INSERT INTO `message` VALUES ('1', '1', 'user', 'user', '{\"message\":\"你好\"}');
INSERT INTO `message` VALUES ('2', '1', 'assistant', 'glm', '你好！');
INSERT INTO `message` VALUES ('3', '1', 'assistant', 'qwen', '你好！很高兴见到你～有什么我可以帮你的吗？?');
INSERT INTO `message` VALUES ('4', '1', 'assistant', 'kimi', '你好！');
INSERT INTO `message` VALUES ('5', '1', 'assistant', 'deepseek', '你好！很高兴见到你。有什么我可以帮助你的吗？?');
INSERT INTO `message` VALUES ('6', '2', 'user', 'user', '{\"message\":\"你好\"}');
INSERT INTO `message` VALUES ('7', '2', 'assistant', 'glm', '你好！');
INSERT INTO `message` VALUES ('8', '2', 'assistant', 'qwen', '你好！很高兴见到你～ ?  \n有什么我可以帮你的吗？无论是问题、想法，还是需要讨论的话题，我都很乐意倾听和协助！');
INSERT INTO `message` VALUES ('9', '2', 'assistant', 'kimi', '你好！');
INSERT INTO `message` VALUES ('10', '2', 'assistant', 'deepseek', '你好！很高兴为你服务。有什么我可以帮你的吗？?');
INSERT INTO `message` VALUES ('11', '3', 'user', 'user', '{\"message\":\"你好\"}');
INSERT INTO `message` VALUES ('12', '3', 'assistant', 'glm', '你好');
INSERT INTO `message` VALUES ('13', '3', 'assistant', 'qwen', '你好！很高兴见到你～有什么我可以帮你的吗？?');
INSERT INTO `message` VALUES ('14', '3', 'assistant', 'kimi', '你好！');
INSERT INTO `message` VALUES ('15', '3', 'assistant', 'deepseek', '你好！有什么可以帮你的吗？?');
INSERT INTO `message` VALUES ('16', '4', 'user', 'user', '{\"message\":\"你可以回复我50字吗\"}');
INSERT INTO `message` VALUES ('17', '4', 'assistant', 'glm', '当然可以，请告诉我您需要回复的内容。');
INSERT INTO `message` VALUES ('18', '4', 'assistant', 'qwen', '当然可以！很高兴为你服务，如有问题、需要帮助或想聊点什么，随时告诉我，我会尽力提供支持与陪伴。');
INSERT INTO `message` VALUES ('19', '4', 'assistant', 'kimi', '好的，可以的。');
INSERT INTO `message` VALUES ('20', '4', 'assistant', 'deepseek', '当然可以！你提到的“回复50字”是要求严格控制在50字内吗？我会尽量精简回答，但需注意标点符号是否计入字数。如果需要，请确认具体规则，我将准确满足你的需求。?');
INSERT INTO `message` VALUES ('21', '5', 'user', 'user', '在');
INSERT INTO `message` VALUES ('22', '5', 'assistant', 'deepseek', '我在。');
INSERT INTO `message` VALUES ('23', '5', 'assistant', 'glm', '请提供具体问题，我将尽力回答。');
INSERT INTO `message` VALUES ('24', '5', 'assistant', 'qwen', '请提供完整问题。');
INSERT INTO `message` VALUES ('25', '5', 'assistant', 'kimi', 'error: 429 Client Error: Too Many Requests for url: https://api.moonshot.cn/v1/chat/completions');
INSERT INTO `message` VALUES ('26', '6', 'user', 'user', '1+1');
INSERT INTO `message` VALUES ('27', '6', 'assistant', 'deepseek', '2');
INSERT INTO `message` VALUES ('28', '6', 'assistant', 'kimi', '2');
INSERT INTO `message` VALUES ('29', '6', 'assistant', 'glm', '2');
INSERT INTO `message` VALUES ('30', '6', 'assistant', 'qwen', '2');
INSERT INTO `message` VALUES ('31', '7', 'user', 'user', '大模型谁厉害');
INSERT INTO `message` VALUES ('32', '7', 'assistant', 'glm', '各有优势，难以一概而论。');
INSERT INTO `message` VALUES ('33', '7', 'assistant', 'kimi', '在人工智能领域，当前最厉害的大模型包括谷歌的BERT、OpenAI的GPT系列和DeepMind的Transformer系列。');
INSERT INTO `message` VALUES ('34', '7', 'assistant', 'deepseek', '目前公认最厉害的通用大模型包括：OpenAI 的 GPT-4、Google 的 Gemini、Anthropic 的 Claude 3、以及中国的 DeepSeek、通义千问和文心一言。不同模型在不同任务上各有优势，没有绝对“最强”。');
INSERT INTO `message` VALUES ('35', '7', 'assistant', 'qwen', '没有绝对“最厉害”的大模型，不同模型在不同任务上各有优势。目前综合能力强的包括GPT-4、Claude 3、Gemini 1.5、Qwen3、Llama 3等。');
INSERT INTO `message` VALUES ('36', '8', 'user', 'user', '记住：我的宠物叫豆豆');
INSERT INTO `message` VALUES ('37', '8', 'assistant', 'glm', '好的，我会记住你的宠物叫豆豆。');
INSERT INTO `message` VALUES ('38', '8', 'assistant', 'deepseek', '好的，记住了。');
INSERT INTO `message` VALUES ('39', '8', 'assistant', 'kimi', '好的，记住了。');
INSERT INTO `message` VALUES ('40', '8', 'assistant', 'qwen', '好的，豆豆！');
INSERT INTO `message` VALUES ('41', '8', 'user', 'user', '我的宠物叫什么？');
INSERT INTO `message` VALUES ('42', '8', 'assistant', 'glm', '豆豆');
INSERT INTO `message` VALUES ('43', '8', 'assistant', 'deepseek', '你的宠物叫豆豆。');
INSERT INTO `message` VALUES ('44', '8', 'assistant', 'kimi', '豆豆。');
INSERT INTO `message` VALUES ('45', '8', 'assistant', 'qwen', '豆豆');
INSERT INTO `message` VALUES ('46', '9', 'user', 'user', '我是包子');
INSERT INTO `message` VALUES ('47', '9', 'assistant', 'deepseek', '你好！请问有什么可以帮你的？');
INSERT INTO `message` VALUES ('48', '9', 'assistant', 'glm', '你好，包子！有什么可以帮助你的吗？');
INSERT INTO `message` VALUES ('49', '9', 'assistant', 'qwen', '你好，包子！?');
INSERT INTO `message` VALUES ('50', '9', 'assistant', 'kimi', 'error: 429 Client Error: Too Many Requests for url: https://api.moonshot.cn/v1/chat/completions');
INSERT INTO `message` VALUES ('51', '9', 'user', 'user', '我是谁');
INSERT INTO `message` VALUES ('52', '9', 'assistant', 'deepseek', '你刚才提到自己是“包子”。如果这是你的自称或昵称，那么你就是“包子”。如果需要确认真实身份，请提供更多信息。');
INSERT INTO `message` VALUES ('53', '9', 'assistant', 'qwen', '你是包子！?');
INSERT INTO `message` VALUES ('54', '9', 'assistant', 'glm', '你自称是“包子”，可能是在开玩笑或者自嘲。如果你需要帮助确定身份或者有其他问题，请提供更多信息。');
INSERT INTO `message` VALUES ('55', '9', 'assistant', 'kimi', '你是包子。');
INSERT INTO `message` VALUES ('56', '9', 'user', 'user', '你好');
INSERT INTO `message` VALUES ('57', '9', 'assistant', 'glm', '你好！有什么我可以帮助你的吗？');
INSERT INTO `message` VALUES ('58', '9', 'assistant', 'deepseek', '你好！有什么可以帮你的吗？');
INSERT INTO `message` VALUES ('59', '9', 'assistant', 'qwen', '你好，包子！?');
INSERT INTO `message` VALUES ('60', '9', 'assistant', 'kimi', '你好！有什么可以帮助你的吗？');
INSERT INTO `message` VALUES ('61', '9', 'user', 'user', '你好');
INSERT INTO `message` VALUES ('62', '9', 'assistant', 'glm', '模型暂不可用');
INSERT INTO `message` VALUES ('63', '9', 'assistant', 'deepseek', '模型暂不可用');
INSERT INTO `message` VALUES ('64', '9', 'assistant', 'kimi', '模型暂不可用');
INSERT INTO `message` VALUES ('65', '9', 'assistant', 'qwen', '你好，包子！?');
INSERT INTO `message` VALUES ('66', '9', 'user', 'user', 'hello');
INSERT INTO `message` VALUES ('67', '9', 'assistant', 'glm', '模型暂不可用');
INSERT INTO `message` VALUES ('68', '9', 'assistant', 'kimi', '模型暂不可用');
INSERT INTO `message` VALUES ('69', '9', 'assistant', 'qwen', 'Hello，包子！?');
INSERT INTO `message` VALUES ('70', '9', 'assistant', 'deepseek', '模型暂不可用');
INSERT INTO `message` VALUES ('71', '9', 'user', 'user', '在吗');
INSERT INTO `message` VALUES ('72', '9', 'assistant', 'glm', '在的，你好！有什么可以帮助你的吗？');
INSERT INTO `message` VALUES ('73', '9', 'assistant', 'kimi', '在的，有什么可以帮你的吗？');
INSERT INTO `message` VALUES ('74', '9', 'assistant', 'deepseek', '在的，请讲。');
INSERT INTO `message` VALUES ('75', '9', 'assistant', 'qwen', '在呢，包子！?');

-- ----------------------------
-- Table structure for session
-- ----------------------------
DROP TABLE IF EXISTS `session`;
CREATE TABLE `session` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_session_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of session
-- ----------------------------
INSERT INTO `session` VALUES ('1', '{\"message\":\"你好\"}');
INSERT INTO `session` VALUES ('2', '{\"message\":\"你好\"}');
INSERT INTO `session` VALUES ('3', '{\"message\":\"你好\"}');
INSERT INTO `session` VALUES ('4', '{\"message\":\"你可以回复我50');
INSERT INTO `session` VALUES ('5', '在');
INSERT INTO `session` VALUES ('6', '1+1');
INSERT INTO `session` VALUES ('7', '大模型谁厉害');
INSERT INTO `session` VALUES ('8', '记住：我的宠物叫豆豆');
INSERT INTO `session` VALUES ('9', '我是包子');
